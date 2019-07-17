import typing

import attr
from attr.validators import instance_of, optional


@attr.s
class Meta:
    """class that represents metadata about a vocal annotation format
    and functions for working with it using Crowsetta

    Attributes
    ----------
    name : str
        name of vocal annotation format. E.g., "textgrid"
    ext : str
        extension of files associated with format, e.g. "TextGrid"
    from_file : typing.Callable
        a function that accepts the name of a file containing
        annotations in the format and returns an Annotation or list of
        Annotations. Required.
    to_csv : typing.Callable
        a function that accepts an Annotation or list of Annotations and
        saves them as a comma-separated value file. Default is None.
    to_format : typing.Callable
        a function that accepts an Annotation or list of Annotations and
        saves files in the format. Default is None.
    module : str
        path to module (a .py file) containing functions for working with format,
        e.g. 'home/users/me/Documents/code/textgrid/textgrid.py'.
        Default is None. Optional; enables format to be loaded without
        making it part of a package that adds it as
        a 'crowsetta.format' entry point in a setup.py file.
    """
    name = attr.ib(validator=instance_of(str))
    ext = attr.ib(validator=instance_of(str))
    from_file = attr.ib(validator=instance_of(typing.Callable))
    to_csv = attr.ib(validator=optional(instance_of(typing.Callable)), default=None)
    to_format = attr.ib(validator=optional(instance_of(typing.Callable)), default=None)
    module = attr.ib(validator=optional(instance_of(str)), default=None)
