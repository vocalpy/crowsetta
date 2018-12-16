import os
from configparser import ConfigParser
from importlib import import_module

HERE = os.path.dirname(__file__)
CONBIRT_CONFIG = ConfigParser()
CONBIRT_CONFIG.read(os.path.join(HERE, 'config.ini'))


CONFIG_DICT_KEYS = {'module', 'to_seq', 'to_csv'}

class Crowsetta:
    """class that handles conversion from different annotation formats into
    lists of Sequence objects and/or csv files"""
    def __init__(self, format=None, extra_config=None):
        self._config = CONBIRT_CONFIG
        if format is not None:
            if type(format) != str:
                raise TypeError(f'format should be a string, not {type(format}')
            _validate_format(format)
        self.format = format

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

        self._funcmap = {}
        for section in self._config.sections():
            this_format_funcmap = {}
            this_format_module = import_module(self._config[section]['module'])
            this_format_funcmap['to_seq'] = getattr(this_format_module,
                                                    self._config[section]['to_seq'])
            this_format_funcmap['to_csv'] = getattr(this_format_module,
                                                    self._config[section]['to_csv'])


    def _validate_format(self, format):
        if format.lower() not in self.config.keys()

    def _to_seq(self, format):

    def to_seq(self, file, format=None):
        if format is None:
            format = _guess_format(file)
        else:
            _validate_format(format)

        for file in files:
            seq = func(file)

    def to_csv(self, file, format=None):
        pass

    def to_format(self, file, to_format, format=None):
        pass