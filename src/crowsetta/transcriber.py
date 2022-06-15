import inspect
from typing import Union
import warnings


class Transcriber:
    """A single class for working with all annotation formats in ``crowsetta``,  
    making it possible to load multiple files from a single ``Transcriber``, 
    without needing to know the names of classes that represent formats.

    converts into ``Annotation`` instances
    (the data structure used to work with annotations and
    convert between formats), and save annotations to
    comma-separated values (csv) files or other file formats.

    Attributes
    ----------
    format : str or class
        If a string, name of vocal annotation format that ``Transcriber`` will use.
        Must be  one of ``crowsetta.formats``.
        If a class, must be either sequence-like or bounding-box-like, i.e.,
        registered as either `crowsetta.interface.SeqLike`` or ``crowsetta.interface.BBoxLike``.

    Methods
    -------
    from_file : Loads annotations from a file
    """
    def __init__(self,
                 format: 'Union[str, crowsetta.interface.SeqLike, crowsetta.interface.BBoxLike]'):
        """make a new ``Transcriber``

        Parameters
        ----------
        format : str or class
            If a string, name of vocal annotation format that ``Transcriber`` will use.
            Must be one of ``crowsetta.formats``.
            If a class, must be either sequence-like or bounding-box-like, i.e.,
            registered as either `crowsetta.interface.SeqLike`` or ``crowsetta.interface.BBoxLike``.
        """
        # avoid circular imports
        from . import (
            formats,
            interface,
        )

        if isinstance(format, str):
            if format not in formats.FORMATS:
                raise ValueError(
                    f"Format name '{format}' not recognized."
                    f"Valid format names:\n{formats.as_list()}"
                )
            if format == 'csv':
                warnings.warn(
                    "The format 'csv' has been renamed to 'generic-seq', "
                    "and the name 'csv' will stop working in the next version. "
                    "Please change any usages of the name 'csv' to 'generic-seq'` now.",
                    FutureWarning,
                )
            _format_class = formats.by_name(format)
        elif inspect.isclass(format):
            if not issubclass(format, interface.BaseFormat):
                raise TypeError(
                    f'Format recognized as a class, but it is not a subclass of ``crowsetta.interface.BaseFormat``.'
                    f'Please ``register`` the class as a subclass of either ``crowsetta.interface.SeqLike`` or '
                    f'``crowsetta.interface.BBoxLike``'
                )
            _format_class = format
        else:
            raise ValueError(
                f"Invalid value for ``format``: {format}"
            )
        self.format = format
        self._format_class = _format_class

    def __repr__(self):
        return f"crowsetta.Transcriber(format='{self.format}')"

    def from_file(self,
                  annot_path,
                  *args,
                  **kwargs
                  ) -> 'Union[crowsetta.interface.SeqLike,crowsetta.interface.BBoxLike]':
        """Load annotations from a file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            path to annotations file

        Returns
        -------
        annotations : class-instance
            an instance of the class referred to by ``self.format``,
            with annotations loaded from ``annot_path``
        """
        return self._format_class.from_file(annot_path, *args, **kwargs)
