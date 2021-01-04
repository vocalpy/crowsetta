import os
from importlib import import_module
import importlib.util

from .csv import toannot_func_to_csv
from . import formats
from .meta import Meta

HERE = os.path.dirname(__file__)

VALID_CONFIG_DICT_KEYS = {'module', 'from_file', 'to_csv', 'to_format'}
REQUIRED_CONFIG_DICT_KEYS = {'module', 'from_file'}


def not_implemented(*args, **kwargs):
    raise NotImplementedError


class Transcriber:
    """class that loads vocal annotation files into Annotations
    (the data structure used to work with annotations and enable
    conversion between formats), and converts Annotations to
    comma-separated values (csv) files or other formats.

    Attributes
    ----------
    format : str
        name of vocal annotation format that Transcriber will use
    config : dict or crowsetta.meta.Meta
        configuration for a format. Default is None.
        Enables user to define a format without creating a Python package.

    Methods
    -------
    from_file : loads a file, returns an Annotation for that file
    to_csv : converts a file in the format into a comma-separate values (csv) file
    to_format : converts an Annotation to the format
    """
    def __init__(self, format, config=None):
        """__init__ method of Transciber class

        Parameters
        ----------
        format : str
            name of format

        Examples
        --------
        >>> my_config = {
        ...     'module': convert_myformat.py
        ...     'from_file': 'myformat2seq',
        ...     'to_csv': 'myformat2csv',
        ...     'to_format': 'to_myformat'
        ... }
        >>> scribe = crowsetta.Transcriber(format='myformat_name', config=my_config)
        >>> seq = scribe.from_file(file='my_annotation.mat')
        """
        # make sure format specified is either installed or that user also specified a config
        if (format in formats._INSTALLED and config is None) or (format and config is not None):
            self.voc_format = format
        else:
            raise ValueError(f"specified vocal annotation format, {format}, not installed, and no"
                             "configuration was specified. Either install format, or specify configuration "
                             "by passing as the 'config' argument to Transcriber")

        # make sure config is valid type
        if config is not None:
            if type(config) != dict and type(config) != Meta:
                raise TypeError(
                    "argument passed for config should be either a dict or "
                    f"an instance of crowsetta.Meta, but was a {type(config)}"
                )

            # and if it's a dict it should have the right keys
            if type(config) == dict:
                config_keys = set(config.keys())
                if not REQUIRED_CONFIG_DICT_KEYS.issubset(config_keys):
                    missing_keys = REQUIRED_CONFIG_DICT_KEYS - config_keys
                    raise KeyError(f'config for {format} requires '
                                   f'the following keys: {missing_keys}')
                elif not config_keys.issubset(VALID_CONFIG_DICT_KEYS):
                    extra_keys = config_keys - VALID_CONFIG_DICT_KEYS
                    raise KeyError(f'config for {format} contains '
                                   f'invalid keys: {extra_keys}')

        if format in formats._INSTALLED and config is None:
            voc_format_module = getattr(formats, format)
            self.from_file = voc_format_module.meta.from_file
            if hasattr(voc_format_module.meta, 'to_csv'):
                self.to_csv = voc_format_module.meta.to_csv
            else:
                self.to_csv = not_implemented
            if hasattr(voc_format_module.meta, 'to_format'):
                self.to_format = voc_format_module.meta.to_format
            else:
                self.to_format = not_implemented

        elif format and config:
            self.config = config
            format_module = config['module']

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

            self.from_file = getattr(this_format_module, config['from_file'])
            # if to_csv not in config (not specified by user)
            if 'to_csv' not in config:
                # default to function returned by toseq_func_to_csv()
                # when we pass it from_file
                self.to_csv = toannot_func_to_csv(self.from_file)
            elif config['to_csv'] is None:
                self.to_csv = not_implemented
            else:
                self.to_csv = getattr(this_format_module, config['to_csv'])

            if 'to_format' not in config or config['to_format'] is None:
                self.to_format = not_implemented
            else:
                self.to_format = getattr(this_format_module, config['to_format'])
