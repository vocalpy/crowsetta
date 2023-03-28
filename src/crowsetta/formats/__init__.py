from __future__ import annotations

import inspect
from typing import Type

from .. import interface
from . import bbox, seq

FORMATS = {}
for module in (bbox, seq):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if inspect.isclass(attr):
            if issubclass(attr, interface.seq.SeqLike) or issubclass(attr, interface.bbox.BBoxLike):
                # note we use the class-level ``name`` attribute, a string, as keys in the dictionary
                FORMATS[attr.name] = attr


__all__ = ["bbox", "FORMATS", "seq"]


def by_name(name: str) -> Type:
    """Get an annotation class by its string name

    Parameters
    ----------
    name : str
        Shorthand name for an annotation format, e.g. 'timit'

    Returns
    -------
    format : class

    Examples
    --------
    >>> import crowsetta
    >>> crowsetta.formats.by_name('timit')
    <class 'crowsetta.formats.seq.timit.Timit'>
    """
    try:
        return FORMATS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def as_list() -> list[str]:
    """List available annotation formats.

    Returns
    -------
    formats : list
        A list of strings,
        shorthand names that can be used
        to access the class by calling
        by their shorthand names

    Examples
    --------
    >>> import crowsetta
    >>> crowsetta.formats.as_list()
    ['aud-bbox', 'aud-seq', 'birdsong-recognition-dataset', 'generic-seq', 'notmat', 'raven', 'simple-seq', 'textgrid', 'timit', 'yarden']  # noqa
    """
    return sorted(FORMATS.keys())


def register_format(format_class: Type) -> Type:
    """Decorator to register annotation formats.

    Adds class to :mod:`crowsetta.formats`.
    The decorator maps the class variable ``name``,
    a string, to the class itself, so that calling
    :func:`crowsetta.formats.by_name` with that string
    will return the class.

    Parameters
    ----------
    format_class : class
        A class that has the required class variables
        and adheres to one of the interfaces
        defined in :mod:`crowsetta.interface`,
        either :class:`~crowsetta.interface.seq.SeqLike`
        or :class:`~crowsetta.interface.bbox.BBoxLike`.

    Returns
    -------
    format_class : class
        The same class, unchanged.
        This decorator only adds the class
        to :data:`crowsetta.formats.FORMATS`.
    """
    if not issubclass(format_class, interface.seq.SeqLike) and not issubclass(format_class, interface.bbox.BBoxLike):
        raise TypeError(f"format class must be subclass of SeqLike or BBoxLike, but was not: {format_class}")
    FORMATS[format_class.name] = format_class
    return format_class
