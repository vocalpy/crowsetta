import os
from configparser import ConfigParser
from importlib import import_module
import importlib.util
import typing

import attr

from .csv import csv2seq

HERE = os.path.dirname(__file__)

VALID_CONFIG_DICT_KEYS = {'module', 'to_seq', 'to_csv', 'to_format'}
REQUIRED_CONFIG_DICT_KEYS = {'module', 'to_seq'}


@attr.s(auto_attribs=True)
class FormatFunctions:
    """functions for converting a given format"""
    to_seq: typing.Callable
    to_csv: typing.Callable
    to_format: typing.Callable


class Transcriber:
    """converts birdsong annotation files into Sequences (the data structure used to enable
    conversion between formats), comma-separated values (csv) files,
    other annotation formats.

    Attributes
    ----------
    _config : ConfigParser
        contains configuration that tells Transciber which functions to use for
        which formats
    file_formats : list
        of str, the formats that an instance of the Transcriber class knows how
        to parse and convert
    format_functions : dict
        that maps each format from file_formats to three functions: a 'to_csv'
        function that converts that format to a csv file, a 'to_seq' function
        that converts it to a Sequence or list of Sequences, and a 'to_format'
        function that maps a Sequence or list of Sequences to that file format

    Methods
    -------
    to_seq : maps a file of a specified format to a Sequence or list of Sequences
    to_csv : maps a file of a specified format to a comma-separate values (csv) file
    to_format : maps a file of a specified format to another format
    from_csv: loads and parses a comma-separated values (csv) file, returns Sequence
    or list of Sequence
    """
    def __init__(self, user_config=None):
        """__init__ method of Transciber class

        Parameters
        ----------
        user_config : dict
            a user-provided dictionary that maps format names to a another
            dictionary that defines the following key-value pairs:
                module: str
                    Required. Name of module from which functions for working with
                    this format will be imported.
                to_seq: Callable
                    Required. Name of function in module that converts this format
                    to sequences
                to_csv: Callable
                    Optional. Name of function in module that converts this format
                    to comma-separated values files.
                to_format: Callable
                    Optional. Name of function in module that converts Sequence objects
                    to this format. Can be None, in which case trying to convert to
                    this format will raise an error.

        Examples
        --------
        >>> my_config = {
        ...     'myformat_name': {
        ...         'module': convert_myformat.py
        ...         'to_seq': 'myformat2seq',
        ...         'to_csv': 'myformat2csv',
        ...         'to_format': 'to_myformat'
        ...     }
        ... }
        >>> scribe = crowsetta.Transcriber(user_config=my_config)
        >>> seq = scribe.toseq(file='my_annotation.mat', file_format='myformat_name')
        """
        # read default config is declared in src/crowsetta/config.ini;
        # have to read  it in __init__ so config doesn't live at module level;
        # otherwise it will be shared across instances (and mutable!)
        crowsetta_config = ConfigParser()
        crowsetta_config.read(os.path.join(HERE, 'config.ini'))
        self._config = crowsetta_config

        if user_config is not None:
            if type(user_config) != dict:
                raise TypeError(f'config_dict should be a dictionary, '
                                f'not {type(user_config)}')

            if not all([type(config_dict) == dict 
                        for config_dict in user_config.values()]):
                not_dict = [config_dict for config_dict in user_config.values()
                            if not type(config_dict) == dict]
                raise TypeError('user_config should be a dictionary of dictionaries,\n'
                                'where keys are format names and values are the dictionary '
                                'that specifies what module and functions to use.\n'
                                f'The following values are not dictionaries: {not_dict}')

            for config_name, config_dict in user_config.items():
                this_config_keys = set(config_dict.keys())
                if not REQUIRED_CONFIG_DICT_KEYS.issubset(this_config_keys):
                    missing_keys = REQUIRED_CONFIG_DICT_KEYS - this_config_keys
                    raise KeyError(f'config_dict for {config_name} requires '
                                   f'the following keys: {missing_keys}')
                elif not this_config_keys.issubset(VALID_CONFIG_DICT_KEYS):
                    extra_keys = this_config_keys - VALID_CONFIG_DICT_KEYS
                    raise KeyError(f'config_dict for {config_name} contains '
                                   f'invalid keys: {extra_keys}')
                self._config.add_section(config_name)
                for option, value in config_dict.items():
                    if value is None:
                        # value has to be a string
                        value = 'None'
                    self._config[config_name][option] = value
                # since these aren't required, have to add default 'None'
                # if user doesn't specify
                if 'to_csv' not in config_dict:
                    self._config[config_name]['to_csv'] = 'None'
                if 'to_format' not in config_dict:
                    self._config[config_name]['to_format'] = 'None'

        self.file_formats = self._config.sections()

        self.format_functions = {}
        for section in self._config.sections():
            format_module = self._config[section]['module']

            if os.path.isfile(format_module):
                # if it's a file (e.g. some path), have to import
                # this more verbose way
                module_name = os.path.basename(format_module)
                if module_name.endswith('.py'):
                    module_name = module_name.replace('.py', '')
                spec = importlib.util.spec_from_file_location(name=module_name,
                                                              location=format_module)
                this_format_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(this_format_module)

            else:
                # if it's not a file, it should be on the path or in the
                # current directory, and we can just import it in one line
                try:
                    this_format_module = import_module(format_module)
                except ModuleNotFoundError:
                    # unless that didn't work either, in which case...
                    raise FileNotFoundError(
                        f'{format_module} could not be imported, '
                        'and not recognized as a file')

            # insert error checking for module attributes (i.e. functions) here
            # so we can give user human-interpretable error messages
            self.format_functions[section] = FormatFunctions(
                to_seq=getattr(this_format_module,
                               self._config[section]['to_seq'],
                               None),
                to_csv=getattr(this_format_module,
                               self._config[section]['to_csv'],
                               None),
                to_format=getattr(this_format_module,
                                  self._config[section]['to_format'],
                                  None),
            )

    def _validate_format(self, file_format):
        """helper function to validate formats specfied by user when
        calling to_seq, to_csv, or to_format methods"""
        if file_format.lower() not in self.file_formats:
            raise ValueError(f'format {file_format} is not recognized.\n'
                             f'Valid formats are: {self.file_formats}')

    def _guess_format(self, file):
        """helper function that tries to guess file format from file
        extensions"""
        if type(file) == str:
            file = [file]

        if all([filename.endswith('.not.mat') for filename in file]):
            return 'notmat'
        elif all([filename.endswith('.xml') for filename in file]):
            return 'koumura'
        else:
            raise ValueError('format not recognized')

    def to_seq(self, file, file_format=None, **kwargs):
        """convert a file or files to a Sequence or list of Sequences

        Parameters
        ----------
        file : str, pathlib.Path, or list
            Name or full path to one annotation file, or a list of such file names or paths
        file_format : str
            Format of file(s). Default is None, in which case an attempt is made to determine
            the format from the file extension.
        **kwargs
            Arbitrary keyword arguments. For when the to_seq function for the format specified
            requires additional arguments.

        Returns
        -------
        seq : Sequence or list of Sequence objects
            A list of Sequence objects is returned when file is a list or if the to_seq function
            can return multiple sequences from a single file based on some arguments
            (as is the case with the crowsetta.koumura.koumura2seq function)

        Examples
        --------
        >>> scribe = crowsetta.Transcriber()
        >>> seq = scribe.to_seq(file='Annotation.xml', file_format='koumura', wavpath='./Data/Wave')
        >>> print(seq[1])
        Sequence(file='0.wav', onsets_Hz=array([ 34240,  40256,  46944,  ...
        """
        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

        return self.format_functions[file_format].to_seq(file, **kwargs)

    def to_csv(self, file, file_format=None, **kwargs):
        """convert a file or files to a comma-separated values (csv) file

        Parameters
        ----------
        file : str or list
            Name or full path to one annotation file, or a list of such file names or paths
        file_format : str
            Format of file(s). Default is None, in which case an attempt is made to determine
            the format from the file extension.
        **kwargs
            Arbitrary keyword arguments. For when the to_csv function for the format specified
            requires additional arguments.

        Returns
        -------
        None

        Examples
        --------
        >>> scribe = crowsetta.Transcriber()
        >>> scribe.to_csv(file='Annotation.xml', file_format='koumura')
        >>> import csv
        >>> with open('Annotation.csv', 'r', newline='') as csv_file:
        ...     reader = csv.reader(csv_file)
        ...     for _ in range(4):
        ...         print(next(reader))
        ...
        ['filename', 'onset_Hz', 'offset_Hz', 'onset_s', 'offset_s', 'label']
        ['0.wav', '34240', '36928', '1.07', '1.154', '0']
        ['0.wav', '40256', '43040', '1.258', '1.345', '0']
        ['0.wav', '46944', '49760', '1.467', '1.555', '0']
        """
        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

        if self.format_functions[file_format].to_csv is None:
            raise NotImplementedError(f'No to_csv function for format: {file_format}')
        else:
            return self.format_functions[file_format].to_csv(file, **kwargs)

    def to_format(self, file, to_format, file_format=None,
                  to_seq_kwargs=None, to_format_kwargs=None):
        """convert a file or files to a file or files in another annotation format

        Parameters
        ----------
        file : str or list
            Name or full path to one annotation file, or a list of such file names or paths
        to_format : str
            Format which file should be converted **to**.
        file_format : str
            Format of file(s). Default is None, in which case an attempt is made to determine
            the format from the file extension.
        to_seq_kwargs : dict
            A dictionary mapping keyword names to values that will be passed to the to_seq
            function for the "from" format,
            i.e. self.format_functions[file_format].to_seq
        to_format_kwargs : dict
            A dictionary mapping keyword names to values that will be passed to the to_format
            function for the "to" format,
            i.e. self.format_functions[to_format].to_format

        Returns
        -------
        None
        """
        if to_format not in self.file_formats:
            raise ValueError(f"cannot convert to format '{to_format}', "
                             f"file format not recognized.\n"
                             f"Valid file formats are: {self.file_formats}")
        elif self.format_functions[to_format].to_format is None:
            raise NotImplementedError("the current configuration does not define "
                                      "a function mapping Sequences to the format"
                                      f" '{to_format}'.")

        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

        # if called w/out kwargs, change default to a mapping
        # so the dictionary unpacking operators don't cause a crash below
        if to_seq_kwargs is None:
            to_seq_kwargs = {}
        if to_format_kwargs is None:
            to_format_kwargs = {}

        seq = self.format_functions[file_format].to_seq(file, **to_seq_kwargs)
        return self.format_functions[to_format].to_format(seq, **to_format_kwargs)

    def from_csv(self, csv_filename):
        """loads and parses a comma-separated values (csv) file,
        returns Sequence or list of Sequence

        Parameters
        ----------
        csv_filename : str

        Returns
        -------
        seq : Sequence or list
        """
        return csv2seq(csv_filename)
