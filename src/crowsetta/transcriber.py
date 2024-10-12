import inspect
import warnings
from typing import Union


class Transcriber:
    """The :class:`crowsetta.Transcriber` class provides a
    way to work with all annotation formats in :mod:`crowsetta`,
    without needing to know the names of classes that represent formats
    (e.g., :class:`crowsetta.formats.seq.AudSeq` or
    :class:`crowsetta.formats.bbox.Raven`.)

    When you make a :class:`~crowsetta.Transcriber` instance,
    you specify its `format` as a string name,
    one of the names returned by :func:`crowsetta.formats.as_list`.

    You can then use this :class:`~crowsetta.Transcriber` instance
    to load multiple annotation files in that ``format``,
    by calling the :meth:`~crowsetta.Transcriber.from_file` method
    repeatedly, e.g., in a for loop or list comprehension.
    This will create multiple instances of the classes that represent
    annotation format, one instance for each annotation file.
    With method chaining you can convert each loaded file at the same time
    to :class:`crowsetta.Annotation`s
    (the data structure used to work with annotations and
    convert between formats), and save annotations to
    comma-separated values (csv) files or other file formats.
    See examples below.

    Attributes
    ----------
    format : str or class
        If a string, name of annotation format that the
        :class:`~crowsetta.Transcriber` will use.
        Must be one of the shorthand string names returned by
        :func:`crowsetta.formats.as_list`.
        If a class, must be one of the classes in
        :mod:`crowsetta.formats` that the shorthand strings refer to.
        You can register your own class using
        :func:`crowsetta.formats.register_format`.
        All format classes must be
        either sequence-like or bounding-box-like, i.e.,
        registered as either
        :class:`crowsetta.interface.seq.SeqLike` or
        :class:`crowsetta.interface.bbox.BBoxLike`.
    Methods
    -------
    from_file : Loads annotations from a file

    Examples
    --------
    An example of loading a sequence-like format with the
    :meth:`~crowsetta.Transcriber.from_file` method.

    >>> import crowsetta
    >>> scribe = crowsetta.Transcriber(format='aud-seq')
    >>> example = crowsetta.example('aud-seq')
    >>> audseq = scribe.from_file(example.annot_path)
    >>> annot = audseq.to_annot()
    >>> annot
    Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/audseq/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None, seq=<Sequence with 61 segments>)  # noqa

    An example of loading a bounding box-like format with the
    :meth:`~crowsetta.Transcriber.from_file` method.
    Notice this format has a parameter ``annot_col`` we need to specify for it to load correctly.
    We can pass this additional parameter into the ``from_file`` method
    as a keyword argument.

    >>> import crowsetta
    >>> scribe = crowsetta.Transcriber(format='raven')
    >>> example = crowsetta.example('raven')
    >>> raven = scribe.from_file(example.annot_path, annot_col='Species')
    >>> annot = raven.to_annot()
    >>> annot
    Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/raven/Recording_1_Segment_02.Table.1.selections.txt'), notated_path=None, bboxes=[BBox(onset=154.387792767, offset=154.911598217, low_freq=2878.2, high_freq=4049.0, label='EATO'), BBox(onset=167.526598245, offset=168.17302044, low_freq=2731.9, high_freq=3902.7, label='EATO'), BBox(onset=183.609636834, offset=184.097751553, low_freq=2878.2, high_freq=3975.8, label='EATO'), BBox(onset=250.527480604, offset=251.160710509, low_freq=2756.2, high_freq=3951.4, label='EATO'), BBox(onset=277.88724277, offset=278.480895806, low_freq=2707.5, high_freq=3975.8, label='EATO'), BBox(onset=295.52970757, offset=296.110168316, low_freq=2951.4, high_freq=3975.8, label='EATO')])  # noqa

    An example of loading a set of annotations in the :class:`~crowsetta.formats.seq.NotMat` format,
    converting them to :class:`~crowsetta.Annotation` instances at the same time with method chaining,
    and then finally saving them as a csv file,
    using the :class:`~crowsetta.formats.seq.GenericSeq` format.

    >>> import pathlib
    >>> import crowsetta
    >>> notmat_paths = sorted(pathlib.Path('./data/bfsongrepo').glob('*.not.mat')
    >>> scribe = crowsetta.Transcriber('notmat')
    >>> # next line, use method chaining to load NotMat and convert to crowsetta.Annotation all at once
    >>> annots = [scribe.from_file(notmat_path).to_annot() for notmat_path in notmat_paths]
    >>> generic_seq = crowsetta.formats.seq.GenericSeq(annots)
    >>> generic_seq.to_csv('./data/bfsongrepo/notmats.csv')
    """

    def __init__(self, format: "Union[str, crowsetta.interface.SeqLike, crowsetta.interface.BBoxLike]"):  # noqa: F821
        """Initialize a new :class:`crowsetta.Transcriber` instance.

        Parameters
        ----------
        format : str or class
            If a string, name of annotation format that the
            :class:`~crowsetta.Transcriber` will use.
            Must be one of the shorthand string names returned by
            :func:`crowsetta.formats.as_list`.
            If a class, must be one of the classes in
            :mod:`crowsetta.formats` that the shorthand strings refer to.
            You can register your own class using
            :func:`crowsetta.formats.register_format`.
            All format classes must be
            either sequence-like or bounding-box-like, i.e.,
            registered as either
            :class:`crowsetta.interface.seq.SeqLike` or
            :class:`crowsetta.interface.bbox.BBoxLike`.
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
                    stacklevel=2,
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
            Path to file containing annotations.

        Returns
        -------
        annotations : class-instance
            An instance of the class referred to by ``self.format``,
            with annotations loaded from ``annot_path``

        Examples
        --------

        An example of loading a sequence-like format with the
        :meth:`~crowsetta.Transcriber.from_file` method.

        >>> import crowsetta
        >>> scribe = crowsetta.Transcriber(format='aud-seq')
        >>> example = crowsetta.example('aud-seq')
        >>> audseq = scribe.from_file(example.annot_path)
        >>> annot = audseq.to_annot()
        >>> annot
        Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/audseq/405_marron1_June_14_2016_69640887.audacity.txt'), notated_path=None, seq=<Sequence with 61 segments>)  # noqa

        An example of loading a bounding box-like format with the
        :meth:`~crowsetta.Transcriber.from_file` method.
        Notice this format has a parameter ``annot_col``
        we need to specify for it to load correctly.
        We can pass this additional parameter into the
        :meth:`~crowsetta.Transcriber.from_file` method
        as a keyword argument.

        >>> import crowsetta
        >>> scribe = crowsetta.Transcriber(format='raven')
        >>> example = crowsetta.example('raven')
        >>> raven = scribe.from_file(example.annot_path, annot_col='Species')
        >>> annot = raven.to_annot()
        >>> annot
        Annotation(annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc1/raven/Recording_1_Segment_02.Table.1.selections.txt'), notated_path=None, bboxes=[BBox(onset=154.387792767, offset=154.911598217, low_freq=2878.2, high_freq=4049.0, label='EATO'), BBox(onset=167.526598245, offset=168.17302044, low_freq=2731.9, high_freq=3902.7, label='EATO'), BBox(onset=183.609636834, offset=184.097751553, low_freq=2878.2, high_freq=3975.8, label='EATO'), BBox(onset=250.527480604, offset=251.160710509, low_freq=2756.2, high_freq=3951.4, label='EATO'), BBox(onset=277.88724277, offset=278.480895806, low_freq=2707.5, high_freq=3975.8, label='EATO'), BBox(onset=295.52970757, offset=296.110168316, low_freq=2951.4, high_freq=3975.8, label='EATO')])  # noqa

        An example of loading a set of annotations in the :class:`~crowsetta.formats.seq.NotMat` format,
        converting them to :class:`~crowsetta.Annotation` instances at the same time with method chaining,
        and then finally saving them as a csv file,
        using the :class:`~crowsetta.formats.seq.GenericSeq` format.

        >>> import pathlib
        >>> import crowsetta
        >>> notmat_paths = sorted(pathlib.Path('./data/bfsongrepo').glob('*.not.mat')
        >>> scribe = crowsetta.Transcriber('notmat')
        >>> # next line, use method chaining to load NotMat and convert to crowsetta.Annotation all at once
        >>> annots = [scribe.from_file(notmat_path).to_annot() for notmat_path in notmat_paths]
        >>> generic_seq = crowsetta.formats.seq.GenericSeq(annots)
        >>> generic_seq.to_csv('./data/bfsongrepo/notmats.csv')
        """
        return self._format_class.from_file(annot_path, *args, **kwargs)
