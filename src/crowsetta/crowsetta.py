import os
from configparser import ConfigParser
from importlib import import_module

HERE = os.path.dirname(__file__)
CROWSETTA_CONFIG = ConfigParser()
CROWSETTA_CONFIG.read(os.path.join(HERE, 'config.ini'))


CONFIG_DICT_KEYS = {'module', 'to_seq', 'to_csv'}


class Crowsetta:
    """class that handles conversion from different annotation formats into
    lists of Sequence objects and/or csv files"""
    def __init__(self, extra_config=None):
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

        self._funcmap = {}
        for section in self._config.sections():
            this_format_funcmap = {}
            this_format_module = import_module(self._config[section]['module'])
            this_format_funcmap['to_seq'] = getattr(this_format_module,
                                                    self._config[section]['to_seq'])
            this_format_funcmap['to_csv'] = getattr(this_format_module,
                                                    self._config[section]['to_csv'])

    def _validate_format(self, file_format):
        if file_format.lower() not in self.file_formats:
            raise ValueError(f'format {file_format} is not recognized.\n'
                             f'Valid formats are: {self.file_formats}')

    def _guess_format(self, file):
        if type(file) == str:
            file = [file]

        if all([filename.endswith('.not.mat') for filename in file]):
            return 'notmat'
        elif all([filename.endswith('.xml') for filename in file]):
            return 'koumura'
        else:
            raise ValueError('format not recognized')

    def to_seq(self, file, file_format=None, **kwargs):
        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

        return self._funcmap[file_format]['to_seq'](file)

    def to_csv(self, file, file_format=None, **kwargs):
        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)

        return self._funcmap[file_format]['to_csv'](file)

    def to_format(self, file, to_format, file_format=None, **kwargs):
        if to_format not in self.file_formats:
            raise ValueError(f"cannot convert to format '{to_format}', "
                             f"file format not recognized.\n"
                             f"Valid file formats are: {self.file_formats}")
        elif self._funcmap['to_format'] is None:
            raise ValueError("the current configuration does not define a function mapping "
                             f"Sequences to the format '{to_format}'.")

        if file_format is None:
            file_format = self._guess_format(file)
        else:
            self._validate_format(file_format)
        seq = self._funcmap[file_format]['to_seq'](file)
        return self._funcmap[to_format]['to_format'](seq)
