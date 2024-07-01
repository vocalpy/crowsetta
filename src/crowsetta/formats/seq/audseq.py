"""module for Audacity LabelTrack
in standard/default format exported to txt files
https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format
"""
import pathlib
from typing import ClassVar, Optional

import attr
import numpy as np
import pandas as pd
import pandera
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike


class AudSeqSchema(pandera.DataFrameModel

):
    """A :class:`pandera.DataFrameModel

`
    that validates :type:`pandas.DataFrame`s
    loaded from Audacity Labeltrack annotations
    exported to txt files in the standard format.

    The standard format is described here:
    https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format
    """

    start_time: Optional[Series[float]] = pandera.Field()
    end_time: Optional[Series[float]] = pandera.Field()
    label: Series[pd.StringDtype] = pandera.Field(coerce=True)

    class Config:
        ordered = True
        strict = True


@crowsetta.interface.SeqLike.register
@attr.define
class AudSeq:
    """Class meant to represent
    Audacity Labeltrack annotations
    exported to txt files in the standard format[1]_.

    The txt file will have 3 tab-separated columns
    that represent the start time, end time, and labels
    of annotated regions.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'aud-seq'``.
    ext: str
        Extension of files in annotation format, ``'.txt'``.
    start_times : numpy.ndarray
        Vector of integer sample numbers corresponding
        to beginning of segments, i.e. onsets.
    end_times : numpy.ndarray
        Vector of integer sample numbers corresponding
        to ends of segments, i.e. offsets.
    labels : numpy.ndarray
        Vector of string labels for segments;
        each element is either a single word,
        or a single phonetic transcription code.
    annot_path : str, pathlib.Path
        Path to file from which annotations were loaded.
    notated_path : str, pathlib.Path
        Path to file that ``annot_path`` annotates.
        E.g., an audio file, or an array file
        that contains a spectrogram generated from audio.
        Optional, default is None.

    References
    ----------
    .. [1^] https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format
    """

    name: ClassVar[str] = "aud-seq"
    ext: ClassVar[str] = ".txt"

    start_times: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    end_times: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    labels: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path
    notated_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls,
        annot_path: PathLike,
        notated_path: Optional[PathLike] = None,
    ) -> "Self":  # noqa: F821
        """Load annotations from a file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to an annotation file,
            with '.txt' extension.
        notated_path : str, pathlib.Path
            Path to file that ``annot_path`` annotates.
            E.g., an audio file, or an array file
            that contains a spectrogram generated from audio.
            Optional, default is None.

        Examples
        --------
        >>> example = crowsetta.data.get('aud-seq')
        >>> audseq = crowsetta.formats.seq.AudSeq.from_file(example.annot_path)
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)
        df = pd.read_csv(annot_path, sep="\t", header=None)
        df.columns = ["start_time", "end_time", "label"]
        df = AudSeqSchema.validate(df)

        return cls(
            start_times=df["start_time"].values,
            end_times=df["end_time"].values,
            labels=df["label"].values,
            annot_path=annot_path,
            notated_path=notated_path,
        )

    def to_seq(self, round_times: bool = True, decimals: int = 3) -> crowsetta.Sequence:
        """Convert this annotation to a :class:`crowsetta.Sequence`.

        Parameters
        ----------
        round_times : bool
            If True, round ``onsets_s`` and ``offsets_s``.
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
        >>> example = crowsetta.data.get('aud-seq')
        >>> audseq = crowsetta.formats.seq.AudSeq.from_file(example.annot_path)
        >>> seq = audseq.to_seq()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        if round_times:
            onsets_s = np.around(self.start_times, decimals=decimals)
            offsets_s = np.around(self.end_times, decimals=decimals)
        else:
            onsets_s = self.start_times
            offsets_s = self.end_times

        seq = crowsetta.Sequence.from_keyword(labels=self.labels, onsets_s=onsets_s, offsets_s=offsets_s)
        return seq

    def to_annot(self, round_times: bool = True, decimals: int = 3) -> crowsetta.Annotation:
        """Convert this annotation to a :class:`crowsetta.Annotation`.

        Parameters
        ----------
        round_times : bool
            If True, round onsets_s and offsets_s.
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
        >>> example = crowsetta.data.get('aud-seq')
        >>> audseq = crowsetta.formats.seq.AudSeq.from_file(example.annot_path)
        >>> annot = audseq.to_annot()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        seq = self.to_seq(round_times, decimals)
        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.notated_path, seq=seq)

    def to_file(self, annot_path: PathLike) -> None:
        """Save this 'aud-seq' annotation to a txt file
        in the standard/default Audacity LabelTrack format.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path with filename of txt file that should be saved.
        """
        df = pd.DataFrame.from_records(
            {"start_time": self.start_times, "end_time": self.end_times, "label": self.labels}
        )
        df = df[["start_time", "end_time", "label"]]  # put in correct order
        try:
            df = AudSeqSchema.validate(df)
        except pandera.errors.SchemaError as e:
            raise ValueError(
                f"Annotations produced an invalid dataframe, " f"cannot convert to Audacity LabelTrack txt file:\n{df}"
            ) from e
        df.to_csv(annot_path, sep="\t", header=False, index=False)
