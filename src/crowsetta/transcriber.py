import inspect
import warnings
from typing import Union


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

    Examples
    --------

    An example of loading a sequence-like format with the ``from_file`` method.

    >>> import crowsetta
    >>> scribe = crowsetta.Transcriber(format='aud-seq')
    >>> example = crowsetta.data.get('aud-seq')
    >>> audseq = scribe.from_file(example.annot_path)
    >>> annot = audseq.to_annot()
    >>> annot
    Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/audseq/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None, seq=<Sequence with 61 segments>)  # noqa

    An example of loading a bounding box-like format with the ``from_file`` method.
    Notice this format has a parameter ``annot_col`` we need to specify for it to load correctly.
    We can pass this additional parameter into the ``from_file`` method
    as a keyword argument.

    >>> import crowsetta
    >>> scribe = crowsetta.Transcriber(format='raven')
    >>> example = crowsetta.data.get('raven')
    >>> raven = scribe.from_file(example.annot_path, annot_col='Species')
    >>> annot = raven.to_annot()
    >>> annot
    Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/raven/Recording_1_Segment_02.Table.1.selections.txt'), notated_path=None, bboxes=[BBox(onset=154.387792767, offset=154.911598217, low_freq=2878.2, high_freq=4049.0, label='EATO'), BBox(onset=167.526598245, offset=168.17302044, low_freq=2731.9, high_freq=3902.7, label='EATO'), BBox(onset=183.609636834, offset=184.097751553, low_freq=2878.2, high_freq=3975.8, label='EATO'), BBox(onset=250.527480604, offset=251.160710509, low_freq=2756.2, high_freq=3951.4, label='EATO'), BBox(onset=277.88724277, offset=278.480895806, low_freq=2707.5, high_freq=3975.8, label='EATO'), BBox(onset=295.52970757, offset=296.110168316, low_freq=2951.4, high_freq=3975.8, label='EATO')])  # noqa
    """

    def __init__(self, format: "Union[str, crowsetta.interface.SeqLike, crowsetta.interface.BBoxLike]"):  # noqa: F821
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
        from . import formats, interface

        if isinstance(format, str):
            if format not in formats.FORMATS:
                raise ValueError(f"Format name '{format}' not recognized." f"Valid format names:\n{formats.as_list()}")
            if format == "csv":
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
                    "Format recognized as a class, but it is not a subclass of ``crowsetta.interface.BaseFormat``."
                    "Please ``register`` the class as a subclass of either ``crowsetta.interface.SeqLike`` or "
                    f"``crowsetta.interface.BBoxLike``. Class was: {format}"
                )
            _format_class = format
        else:
            raise ValueError(f"Invalid value for ``format``: {format}")
        self.format = format
        self._format_class = _format_class

    def __repr__(self):
        return f"crowsetta.Transcriber(format='{self.format}')"

    def from_file(
        self, annot_path, *args, **kwargs
    ) -> "Union[crowsetta.interface.SeqLike,crowsetta.interface.BBoxLike]":  # noqa: F821
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

        Examples
        --------

        An example of loading a sequence-like format with the ``from_file`` method.

        >>> import crowsetta
        >>> scribe = crowsetta.Transcriber(format='aud-seq')
        >>> example = crowsetta.data.get('aud-seq')
        >>> audseq = scribe.from_file(example.annot_path)
        >>> annot = audseq.to_annot()
        >>> annot
        Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/audseq/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None, seq=<Sequence with 61 segments>)  # noqa

        An example of loading a bounding box-like format with the ``from_file`` method.
        Notice this format has a parameter ``annot_col`` we need to specify for it to load correctly.
        We can pass this additional parameter into the ``from_file`` method
        as a keyword argument.

        >>> import crowsetta
        >>> scribe = crowsetta.Transcriber(format='raven')
        >>> example = crowsetta.data.get('raven')
        >>> raven = scribe.from_file(example.annot_path, annot_col='Species')
        >>> annot = raven.to_annot()
        >>> annot
        Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/raven/Recording_1_Segment_02.Table.1.selections.txt'), notated_path=None, bboxes=[BBox(onset=154.387792767, offset=154.911598217, low_freq=2878.2, high_freq=4049.0, label='EATO'), BBox(onset=167.526598245, offset=168.17302044, low_freq=2731.9, high_freq=3902.7, label='EATO'), BBox(onset=183.609636834, offset=184.097751553, low_freq=2878.2, high_freq=3975.8, label='EATO'), BBox(onset=250.527480604, offset=251.160710509, low_freq=2756.2, high_freq=3951.4, label='EATO'), BBox(onset=277.88724277, offset=278.480895806, low_freq=2707.5, high_freq=3975.8, label='EATO'), BBox(onset=295.52970757, offset=296.110168316, low_freq=2951.4, high_freq=3975.8, label='EATO')])  # noqa
        """
        return self._format_class.from_file(annot_path, *args, **kwargs)
