import inspect

from .. import interface

from . import (
    bbox,
    seq
)

FORMATS = {}
for module in (bbox, seq):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if inspect.isclass(attr):
            if issubclass(attr, interface.seq.SeqLike) or issubclass(attr, interface.bbox.BBoxLike):
                # note we use the class-level ``name`` attribute, a string, as keys in the dictionary
                FORMATS[attr.name] = attr


def by_name(name):
    """get an annotation class by its string name

    Parameters
    ----------
    name : str
        Shorthand name for an annotation format, e.g. 'timit'

    Returns
    -------
    format : class
    """
    try:
        return FORMATS[name]
    except KeyError:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        ) from None


def as_list():
    """generate a list of available annotation formats.
    List of strings, shorthand names that can be used
    to access the class by calling
    by their shorthand names"""
    return sorted(FORMATS.keys())


def register_format(format_class):
    """Decorator to register annotation formats"""
    if not issubclass(format_class, interface.seq.SeqLike) and not issubclass(format_class, interface.bbox.BBoxLike):
        raise TypeError(
            f'format class must be subclass of SeqLike or BBoxLike, but was not: {format_class}'
        )
    FORMATS[format_class.name] = format_class
    return format_class
