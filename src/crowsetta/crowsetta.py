import os
from configparser import ConfigParser
from importlib import import_module
import typing

import attr

HERE = os.path.dirname(__file__)
CROWSETTA_CONFIG = ConfigParser()
CROWSETTA_CONFIG.read(os.path.join(HERE, 'config.ini'))


CONFIG_DICT_KEYS = {'module', 'to_seq', 'to_csv', 'to_format'}


@attr.s(auto_attribs=True)
class FormatFunctions:
    """functions for converting a given format"""
    to_seq: typing.Callable
    to_csv: typing.Callable
    to_format: typing.Callable


class Crowsetta:
    """converts birdsong annotation files into comma-separated values (csv) files,
    other annotation formats, or Sequences (the data structure used to enable
    conversion between formats).

    Attributes
    ----------
    _config : ConfigParser
        contains configuration that tells Crowsetta which functions to use for
        which formats
    file_formats : list
        of str, the formats that an instance of the Crowsetta class knows how
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
    """
    def __init__(self, extra_config=None):
        """__init__ method of Crowsetta class

        Parameters
        ----------
        extra_config : dict
            a user-provided dictionary that maps format names to a `config_dict`
            that defines the following key-value pairs:
                module: str
                    name of module from which functions for this format can be
                    imported
                to_seq: Callable
                    name of function in module that converts this file format to
                    sequences
                to_csv: Callable
                    name of function in module that converts this file format to
                    comma-separated values files
                to_format: Callable
                    name of function in module that converts Sequence objects to
                    this format. Can be None, in which case trying to convert to
                    this format will raise an error.
        """
        self._config = CROWSETTA_CONFIG

        if extra_config is not None:
            if type(extra_config) != list and type(extra_config) != dict:
                raise TypeError(f'config_dict should be a dictionary '
                                f'or list of dictionaries, not {type(config_dict)}')

            if type(extra_config) is dict:
                extra_config = [extra_config]

            if not all([type(config_dict) == dict for config_dict in extra_config]):
                raise TypeError('all elements in extra_config should be dictionaries '
                                f'with the following keys: {CONFIG_DICT_KEYS}')

            for config_name, config_dict in config_dict.items():
                this_config_keys = set(config_dict.keys())
                if this_config_keys != CONFIG_DICT_KEYS:
                    if this_config_keys < CONFIG_DICT_KEYS:
                        missing_keys = CONFIG_DICT_KEYS - this_config_keys
                        raise KeyError(f'config_dict for {config_name} is missing '
                                       f'the following keys: {missing_keys}')
                    elif this_config_keys > CONFIG_DICT_KEYS:
                        extra_keys = this_config_keys - CONFIG_DICT_KEYS
                        raise KeyError(f'config_dict for {config_name} contains '
                                       f'invalid keys: {extra_keys}')
                self._config.add_section(config_name)
                for option, value in config_dict.items():
                    self._config.set(config_name, option=option, value=value)

        self.file_formats = self._config.sections()

        self.format_functions = {}
        for section in self._config.sections():
            this_format_module = import_module(self._config[section]['module'])
            self.format_functions[section] = FormatFunctions(
                to_seq=getattr(this_format_module, self._config[section]['to_seq']),
                to_csv=getattr(this_format_module, self._config[section]['to_csv']),
                to_format=getattr(this_format_module, self._config[section]['to_format']),
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
        file : str or list
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
        >>> crow = Crowsetta()
        >>> seq = crow.to_seq(file='Annotation.xml', file_format='koumura', wavpath='./Data/Wave')
        >>> print(seq[1])
        Sequence(file='0.wav', onsets_Hz=...
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
        """
        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

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
            raise ValueError("the current configuration does not define a function mapping "
                             f"Sequences to the format '{to_format}'.")

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
