"""Module with functions for working with Praat TextGrid annotation files

Uses the Python library ``textgrid``:
https://github.com/kylebgorman/textgrid
A version is distributed with this code (../textgrid) under MIT license.
https://github.com/kylebgorman/textgrid/blob/master/LICENSE
"""
import pathlib
from typing import ClassVar, Optional

import attr
import numpy as np

import crowsetta
from crowsetta._vendor import textgrid
from crowsetta.typing import PathLike


@crowsetta.interface.SeqLike.register
@attr.define
class TextGrid:
    """Class that represents annotations
    from TextGrid annotation files
    produced by the application Praat.

    See ``Notes`` below for more detail
    for more details on the types of
    TextGrid annotations that this class
    can work with.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'textgrid'``.
    ext: str
        Extension of files in annotation format: ``'.TextGrid'``.
    textgrid : textgrid.TextGrid
        object that contains annotations from the a '.TextGrid' file.
    annot_path : str, pathlib.Path
        Path to TextGrid file from which annotations were loaded.
    audio_path : str, pathlib.Path
        Path to audio file that ``annot_path`` annotates.

    Notes
    -----
    Uses the Python library textgrid
    https://github.com/kylebgorman/textgrid

    A version is distributed with this code (../textgrid) under MIT license
    https://github.com/kylebgorman/textgrid/blob/master/LICENSE

    This class will load any file that the :mod:`~crowsetta._vendor.textgrid` libray can parse,
    but it can only convert Praat IntervalTiers to :class:`crowsetta.Sequence` and
    :class:`crowsetta.Annotation` instances.
    Additionally, it will only convert a single IntervalTier
    (that can be specified when calling :meth:`crowsetta.formats.seq.TextGrid.to_seq`
    or :meth:`crowsetta.formats.seq.TextGrid.to_annot`).
    """

    name: ClassVar[str] = "textgrid"
    ext: ClassVar[str] = ".TextGrid"

    textgrid: textgrid.TextGrid
    annot_path: pathlib.Path
    audio_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls,
        annot_path: PathLike,
        audio_path: Optional[PathLike] = None,
    ) -> "Self":  # noqa: F821
        """Load annotations from a TextGrid file
        in the format used by Praat.

        Parameters
        ----------
        annot_path: str, pathlib.Path
            Path to a TextGrid file in the format used by Praat.
        audio_path : str. pathlib.Path
            Path to audio file that the ``annot_path`` annotates.
            Optional, default is None.

        Examples
        --------
        >>> example = crowsetta.data.get('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        tg = textgrid.TextGrid.fromFile(annot_path)

        return cls(textgrid=tg, annot_path=annot_path, audio_path=audio_path)

    def to_seq(self, interval_tier: int = 0, round_times: bool = True, decimals: int = 3) -> crowsetta.Sequence:
        """Convert an IntervalTier from this TextGrid annotation
        into a :class:`crowsetta.Sequence`.

        Currently, there is only support for converting a single IntervalTier
        to a single :class:`~crowsetta.Sequence`.

        Parameters
        ----------
        interval_tier : int
            Index of IntervalTier in TextGrid file from which annotations
            should be taken. Default is 0, i.e., the first IntervalTier.
            Necessary in cases where files have multiple IntervalTiers.
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
        >>> example = crowsetta.data.get('textgrid')
        >>> textgrid = crowsetta.formats.seq.TextGrid.from_file(example.annot_path)
        >>> seq = textgrid.to_seq()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        intv_tier = self.textgrid[interval_tier]
        if not isinstance(intv_tier, textgrid.IntervalTier):
            raise ValueError(
                f"Index specified for IntervalTier was {interval_tier}, "
                f"but type at that index was {type(intv_tier)}, not an IntervalTier"
            )

        onsets_s = np.asarray([interval.minTime for interval in intv_tier])
        offsets_s = np.asarray([interval.maxTime for interval in intv_tier])
        labels = np.asarray([interval.mark for interval in intv_tier])

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        seq = crowsetta.Sequence.from_keyword(labels=labels, onsets_s=onsets_s, offsets_s=offsets_s)
        return seq

    def to_annot(self, interval_tier: int = 0, round_times: bool = True, decimals: int = 3) -> crowsetta.Annotation:
        """Convert an IntervalTier from this TextGrid annotation
        to a :class:`crowsetta.Annotation`.

        Currently, there is only support for converting a single IntervalTier
        to an :class:`~crowsetta.Annotation` with a single :class:`~crowsetta.Sequence`.

        Parameters
        ----------
        interval_tier : int
            Index of IntervalTier in TextGrid file from which annotations
            should be taken. Default is 0, i.e., the first IntervalTier.
            Necessary in cases where files have multiple IntervalTiers.
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
        >>> example = crowsetta.data.get('textgrid')
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
        seq = self.to_seq(interval_tier=interval_tier, round_times=round_times, decimals=decimals)

        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, seq=seq)
