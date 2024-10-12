"""Module with functions for working with Praat TextGrid annotation files"""

from __future__ import annotations

import pathlib
import reprlib
from typing import ClassVar, Optional, Union

import attr
import numpy as np

import crowsetta
from crowsetta.typing import PathLike

from .classes import IntervalTier, PointTier
from .parse import parse


@crowsetta.interface.SeqLike.register
@attr.define
class TextGrid:
    """Class that represents annotations
    from TextGrid [1]_ files
    produced by the application Praat [2]_.

    This class can load TextGrid files
    saved by Praat as text files,
    in either the default format
    or the "short" format,
    as described in the specification [1]_.
    The class can load either UTF-8 or UTF-16 text files.
    It should detect both the encoding (UTF-8 or UTF-16)
    and the format (default or "short") automatically.

    The class does not currently parse binary TextGrid files
    (althoug there is an issue to add this,
    see https://github.com/vocalpy/crowsetta/issues/242).
    Please "thumbs up" that issue and comment
    if you would find this helpful.

    This class can parse both interval tiers
    and point tiers in TextGrid files,
    but when converting to a
    :class:`crowsetta.Annotation` it can only
    convert :class:`~crowsetta.formats.seq.textgrid.classes.IntervalTier`
    instances to :class:`crowsetta.Sequence` instances.
    See the :meth:`~crowsetta.formats.seq.textgrid.TextGrid.to_seq`
    method for details.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'textgrid'``.
    ext: str
        Extension of files in annotation format: ``'.TextGrid'``.
    xmin: float
        Start time in seconds of this TextGrid.
    xmax: float
        End time in seconds of this TextGrid.
    tiers: list
        The tiers in this TextGrid,
        a list of IntervalTier and/or PointTier instances.
    annot_path : str, pathlib.Path
        The path to the TextGrid file from which annotations were loaded.
    audio_path : str, pathlib.Path
        The path to the audio file that ``annot_path`` annotates.
        Optional, default is None.

    Examples
    --------
    Loading the example textgrid

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> print(textgrid)
    TextGrid(tiers=[PointTier(nam...ark='L+!H-')]), IntervalTier(...aleila\\-^')]), IntervalTier(...t='earlier')])], xmin=0.0, xmax=2.4360509767904546, annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc2/textgrid/AVO-maea-basic.TextGrid'), audio_path=None)  # noqa: E501

    Determining the number of tiers in the textgrid

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> len(textgrid)
    3

    Getting the names of the tiers in the textgrid

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> textgrid.tier_names
    ['Tones', 'Samoan', 'Gloss']

    Getting a tier from the TextGrid by name

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> textgrid['Gloss']
    IntervalTier(name='Gloss', xmin=0.0, xmax=2.4360509767904546, intervals=[Interval(xmin=0.0, xmax=0.051451575248407266, text='PRES'), Interval(xmin=0.051451575248407266, xmax=0.6407379583230295, text='Sione'), Interval(xmin=0.6407379583230295, xmax=0.7544662733943284, text='PAST'), Interval(xmin=0.7544662733943284, xmax=1.244041566788134, text='pull-ES'), Interval(xmin=1.244041566788134, xmax=1.3481058803597676, text='DET'), Interval(xmin=1.3481058803597676, xmax=1.70760078178904, text='rope'), Interval(xmin=1.70760078178904, xmax=2.4360509767904546, text='earlier')])  # noqa: E501

    Getting a tier from the TextGrid by index

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> textgrid[2]  # same tier we just got by name
    IntervalTier(name='Gloss', xmin=0.0, xmax=2.4360509767904546, intervals=[Interval(xmin=0.0, xmax=0.051451575248407266, text='PRES'), Interval(xmin=0.051451575248407266, xmax=0.6407379583230295, text='Sione'), Interval(xmin=0.6407379583230295, xmax=0.7544662733943284, text='PAST'), Interval(xmin=0.7544662733943284, xmax=1.244041566788134, text='pull-ES'), Interval(xmin=1.244041566788134, xmax=1.3481058803597676, text='DET'), Interval(xmin=1.3481058803597676, xmax=1.70760078178904, text='rope'), Interval(xmin=1.70760078178904, xmax=2.4360509767904546, text='earlier')])  # noqa: E501

    Calling the :meth:`~crowsetta.formats.seq.TextGrid.to_seq` method
    with no arguments will convert all interval tiers
    :class:`~crowsetta.Sequence` instances,
    in the order they appear in the TextGrid.

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> textgrid.to_seq()
    [<Sequence with 7 segments>, <Sequence with 7 segments>]

    Call the :meth:`~crowsetta.formats.seq.TextGrid.to_seq` method
    with a ``tier`` argument to convert a specific
    :class:`~crowsetta.formats.seq.textgrid.classes.IntervalTier`s to a
    single :class:`~crowsetta.Sequence` instance.

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> textgrid.to_seq(tier=2)
    [<Sequence with 7 segments>]

    When calling :meth:`~crowsetta.formats.seq.TextGrid.to_seq`
    you can specify the ``tier`` as an int,
    or the name of the tier as a string.
    I.e., this parameter works the same way
    as square bracket access to a TextGrid as shown above.

    >>> textgrid = crowsetta.example('AVO-maea-basic')
    >>> seq1 = textgrid.to_seq(tier=2)
    >>> seq2 = textgrid.to_seq(tier="Gloss")
    >>> seq1 == seq2
    True

    Notes
    -----
    Code for parsing TextGrids is adapted from several sources,
    all under MIT license.
    The main logic in
    :func:`~crowsetta.formats.seq.textgrid.parse.parse_fp`
    is from <https://github.com/dopefishh/pympi>
    which is perhaps the most concise
    Python code I have found for parsing TextGrids.
    However, there are also good ideas in
    https://github.com/kylebgorman/textgrid/blob/master/textgrid/textgrid.py
    (__getitem__ method for tier access) and
    https://github.com/timmahrt/praatIO
    (data classes, handling encoding).

    For some documentation of the binary format see
    https://github.com/Legisign/Praat-textgrids
    and for a citable library with docs see
    https://github.com/hbuschme/TextGridTools
    but note that both of these have a GPL license.

    References
    ----------

    .. [1] https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html

    .. [2]  Boersma, Paul & Weenink, David (2023).
       Praat: doing phonetics by computer [Computer program].
       Version 6.3.09, retrieved 2 March 2023 from http://www.praat.org/
    """

    name: ClassVar[str] = "textgrid"
    ext: ClassVar[str] = ".TextGrid"

    tiers: list[Union[IntervalTier, PointTier]] = attr.field(repr=reprlib.repr)
    xmin: float
    xmax: float
    annot_path: pathlib.Path
    audio_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls,
        annot_path: PathLike,
        audio_path: Optional[PathLike] = None,
        keep_empty: bool = False,
    ) -> "Self":  # noqa: F821
        """Load annotations from a TextGrid file
        in the format used by Praat.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            The path to a TextGrid file from which annotations were loaded.
        audio_path : str, pathlib.Path
            The path to the audio file that ``annot_path`` annotates.
            Optional, default is None.
        keep_empty : bool
            If True, keep intervals in
            interval tiers that have empty labels
            (i.e., the empty string "").
            Default is False.

        Examples
        --------
        >>> path = crowsetta.example('AVO-maea-basic', return_path=True)
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(path)
        >>> print(textgrid)
        TextGrid(tiers=[PointTier(nam...ark='L+!H-')]), IntervalTier(...aleila\\-^')]), IntervalTier(...t='earlier')])], xmin=0.0, xmax=2.4360509767904546, annot_path=PosixPath('/home/pimienta/.local/share/crowsetta/5.0.0rc2/textgrid/AVO-maea-basic.TextGrid'), audio_path=None)  # noqa: E501

        For usage, see the
        "Examples" section in :class:`crowsetta.formats.seq.textgrid.TextGrid`.

        See Also
        --------
        :class:`crowsetta.formats.seq.textgrid.TextGrid`
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        tg_dict = parse(annot_path, keep_empty)

        return cls(
            tiers=tg_dict["tiers"],
            xmin=tg_dict["xmin"],
            xmax=tg_dict["xmax"],
            annot_path=annot_path,
            audio_path=audio_path,
        )

    def __len__(self):
        return len(self.tiers)

    @property
    def tier_names(self):
        return list(tier.name for tier in self.tiers)

    def __getitem__(self, key: Union[str, int, slice]) -> Union[IntervalTier, PointTier]:
        if isinstance(key, str):
            matching_name_inds = [tier_ind for tier_ind, tier in enumerate(self.tiers) if tier.name == key]
            if len(matching_name_inds) > 1:
                raise ValueError(
                    f"Multiple tiers have the name '{key}', tiers are: {matching_name_inds}."
                    "Please access tiers with one of those integer indices, "
                    "or give the tiers unique names to be able to access with a string."
                )
            ind = matching_name_inds[0]
            return self.tiers[ind]

        elif isinstance(key, (int, slice)):
            return self.tiers[key]

        else:
            raise TypeError(f"Tiers must be accessed with a string key or an integer index, but got a {type(key)}.")

    @staticmethod
    def _interval_tier_to_seq(
        interval_tier: IntervalTier, round_times: bool = True, decimals: int = 3
    ) -> crowsetta.Sequence:
        """Helper method used by ``to_seq``
        that converts a single IntervalTier to a ``crowsetta.Sequence``"""
        onsets_s = []
        offsets_s = []
        labels = []

        for interval in interval_tier.intervals:
            xmin, xmax, text = interval.xmin, interval.xmax, interval.text
            onsets_s.append(xmin)
            offsets_s.append(xmax)
            labels.append(text)

        onsets_s = np.array(onsets_s)
        offsets_s = np.array(offsets_s)
        labels = np.array(labels)

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        seq = crowsetta.Sequence.from_keyword(labels=labels, onsets_s=onsets_s, offsets_s=offsets_s)

        return seq

    def to_seq(
        self, tier: int | str | None = None, round_times: bool = True, decimals: int = 3
    ) -> crowsetta.Sequence | list[crowsetta.Sequence]:
        """Convert an IntervalTier from this TextGrid annotation
        into a :class:`crowsetta.Sequence`.

        Currently, there is only support for converting a single IntervalTier
        to a single :class:`~crowsetta.Sequence`.

        Parameters
        ----------
        tier : int
            Index or string name of interval tier in TextGrid file
            from which annotations should be taken.
            Default is None, in which case all interval tiers
            are converted to :class:`crowsetta.Sequence`s.
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.

        Returns
        -------
        seq : crowsetta.Sequence

        Examples
        --------
        Calling the :meth:`~crowsetta.formats.seq.TextGrid.to_seq` method
        with no arguments will convert all interval tiers
        :class:`~crowsetta.Sequence` instances,
        in the order they appear in the TextGrid.

        >>> example = crowsetta.example('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        >>> textgrid.to_seq()
        [<Sequence with 7 segments>, <Sequence with 7 segments>]

        Call the :meth:`~crowsetta.formats.seq.TextGrid.to_seq` method
        with a ``tier`` arguments to convert a specific
        :class:`~crowsetta.formats.seq.textgrid.classes.IntervalTier` to a
        single :class:`~crowsetta.Sequence`.

        >>> example = crowsetta.example('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        >>> textgrid.to_seq(tier=2)
        [<Sequence with 7 segments>]

        When calling :meth:`~crowsetta.formats.seq.TextGrid.to_seq`
        you can specify the ``tier`` as an int,
        or the name of the tier as a string.
        I.e., this parameter works the same way
        as square bracket access to a TextGrid as shown above.

        >>> example = crowsetta.example('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        >>> seq1 = textgrid.to_seq(tier=2)
        >>> seq2 = textgrid.to_seq(tier="Gloss")
        >>> seq1 == seq2
        True

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        if tier is not None:
            tier_ = self.__getitem__(tier)
            if not isinstance(tier_, IntervalTier):
                raise ValueError(
                    f"The specified tier ({tier}) is not an interval tier, type is {type(tier_)}."
                    f"Cannot convert to a crowsetta.Sequence"
                )
            return self._interval_tier_to_seq(tier_, round_times, decimals)

        seq = [
            self._interval_tier_to_seq(tier, round_times, decimals)
            for tier in self.tiers
            if isinstance(tier, IntervalTier)
        ]
        if len(seq) == 1:
            seq = seq[0]

        return seq

    def to_annot(
        self, tier: int | str | None = None, round_times: bool = True, decimals: int = 3
    ) -> crowsetta.Annotation:
        """Convert interval tier or tiers from this TextGrid annotation
        to a :class:`crowsetta.Annotation` with a :data:`seq` attribute.

        Parameters
        ----------
        tier : int
            Index or string name of interval tier in TextGrid file
            from which annotations should be taken.
            Default is None, in which case all interval tiers
            are converted to :class:`crowsetta.Sequence`s.
        round_times : bool
            If True, round times of onsets and offsets.
            Default is True.
        decimals : int
            Number of decimals places to round floating point numbers to.
            Only meaningful if round_times is True.
            Default is 3, so that times are rounded to milliseconds.

        Returns
        -------
        annot : crowsetta.Annotation

        Examples
        --------
        >>> example = crowsetta.example('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        >>> annot = textgrid.to_annot()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        seq = self.to_seq(tier=tier, round_times=round_times, decimals=decimals)

        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, seq=seq)
