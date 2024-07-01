"""Module for Audacity label tracks
in extended format, exported to txt files
https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Extended_format_with_frequency_ranges
"""
from __future__ import annotations

import pathlib
from typing import ClassVar, List, Optional

import attr
import pandas as pd
import pandera
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike


def txt_to_records(aud_txt_path: PathLike) -> list[dict]:
    """Load a txt file in Audacity extended label track format
    into records for a :type:`pandas.DataFrame`.

    Returns a :class:`list` of :class:`dict` that can be made into a
    :class:`~pandas.DataFrame` by calling :meth:`pandas.DataFrame.from_records`.

    Parameters
    ----------
    aud_txt_path : str, pathlib.Path

    Returns
    -------
    records : list
        Of :class:`dict`, each :class:`dict` will become
        a row in the :class:`~pandas.DataFrame`.

    Notes
    -----
    We work with Audacity txt files this way, instead of
    loading with :func:`pandas.read_csv` then munging, so that we can
    be sure that we can round-trip data without corrupting it.
    """
    with pathlib.Path(aud_txt_path).open("r") as fp:
        lines = fp.read().splitlines()
    lines = [line.split("\t") for line in lines]

    records = []
    # next line: iterate over lines in groups of 2
    for row1, row2 in zip(*[iter(lines)] * 2):
        record = {
            "begin_time_s": float(row1[0]),
            "end_time_s": float(row1[1]),
            "label": str(row1[2]),
            "low_freq_hz": float(row2[1]),
            "high_freq_hz": float(row2[2]),
        }
        records.append(record)
    return records


def df_to_lines(df: pd.DataFrame) -> list[str]:
    """Convert a :type:`pandas.DataFrame` to a
    :class:`list` of :class:`str` that can be saved
    as a txt file in Audacity extended
    label track format.

    This function is (roughly) the inverse of
    :func:`crowsetta.formats.bbox.audbbox.txt_to_records`.

    Parameters
    ----------
    df : pandas.DataFrame
        With contents of a txt file in Audacity extended label track format,
        after being loaded and parsed by :func:`crowsetta.formats.bbox.audbbox.audbbox_txt_to_df`

    Returns
    -------
    lines : list
        List of strings that can be saved to a text file
        by calling :func:`writelines`.

    Notes
    -----
    We work with Audacity txt files this way, instead of
    munging and then calling :meth:`pandas.DataFrame.to_csv`,
    so that we can be sure that we can round-trip data
    without corrupting it.
    """
    df = AudBBoxSchema.validate(df)

    lines = []
    for record in df.itertuples():
        row1 = f"{float(record.begin_time_s)}\t{float(record.end_time_s)}\t{record.label}\n"
        row2 = f"\\\t{float(record.low_freq_hz)}\t{float(record.high_freq_hz)}\n"
        lines.extend((row1, row2))

    return lines


class AudBBoxSchema(pandera.DataFrameModel

):
    """A :class:`pandera.DataFrameModel

` that
    validates :mod:`pandas` dataframes
    loaded from Audacity label tracks
    in extended format, exported to txt files
    https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Extended_format_with_frequency_ranges
    """

    begin_time_s: Series[float] = pandera.Field(coerce=True)
    end_time_s: Series[float] = pandera.Field(coerce=True)
    label: Series[pd.StringDtype] = pandera.Field(coerce=True)
    low_freq_hz: Series[float] = pandera.Field(coerce=True)
    high_freq_hz: Series[float] = pandera.Field(coerce=True)

    class Config:
        ordered = True
        strict = True


@crowsetta.interface.BBoxLike.register
@attr.define
class AudBBox:
    """Class that represents Audacity label tracks
    in extended format, exported to txt files
    https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Extended_format_with_frequency_ranges

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: 'aud-bbox'.
    ext: str
        Extension of files in annotation format: '.txt'
    df : pandas.DataFrame
        with annotations loaded into it
    annot_path : str, pathlib.Path
        Path to Audacity txt file from which annotations were loaded.
    audio_path : str. pathlib.Path
        Path to audio file that the Audacity txt file annotates.
    """

    COLUMNS_MAP: ClassVar[dict] = {
        0: "begin_time_s",
        1: "end_time_s",
        2: "label",
        3: "low_freq_hz",
        4: "high_freq_hz",
    }

    name: ClassVar[str] = "aud-bbox"
    ext: ClassVar[str] = ".txt"

    df: pd.DataFrame
    annot_path: pathlib.Path
    audio_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(cls, annot_path: PathLike, audio_path: Optional[PathLike] = None) -> "Self":  # noqa: F821
        """Load annotations from an Audacity annotation file with bounding boxes,
        created by exporting a Selection Table.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to a txt file exported from Audacity bbox.
        audio_path : str, pathlib.Path
            Path to audio file that the Audacity bbox txt file annotates.
            Optional, defaults to None.

        Examples
        --------
        >>> example = crowsetta.data.get('aud-bbox')
        >>> audbbox = crowsetta.formats.bbox.AudBBox.from_file(example.annot_path)
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)
        records = crowsetta.formats.bbox.audbbox.txt_to_records(annot_path)
        df = pd.DataFrame.from_records(records)
        if len(df) < 1:
            raise ValueError(f"Cannot load annotations, " f"there are no rows in Audacity txt file:\n{df}")
        df = crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(df)

        return cls(
            df=df,
            annot_path=annot_path,
            audio_path=audio_path,
        )

    def to_bbox(self) -> List[crowsetta.BBox]:
        """Convert this Audacity extended label track annotation
        to a :class:`list` of :class:`crowsetta.Bbox`.

        Returns
        -------
        bboxes : list
            A :class:`list` of :class:`crowsetta.BBox` instances.

        Examples
        --------
        >>> example = crowsetta.data.get('aud-bbox')
        >>> audbbox = crowsetta.formats.bbox.AudBBox.from_file(example.annot_path)
        >>> bboxes = audbbox.to_bbox()
        """
        bboxes = []
        for begin_time, end_time, label, low_freq, high_freq in zip(
            self.df.begin_time_s.values,
            self.df.end_time_s.values,
            self.df.label.values,
            self.df.low_freq_hz.values,
            self.df.high_freq_hz.values,
        ):
            bboxes.append(
                crowsetta.BBox(onset=begin_time, offset=end_time, low_freq=low_freq, high_freq=high_freq, label=label)
            )
        return bboxes

    def to_annot(self) -> crowsetta.Annotation:
        """Convert this Audacity bbox annotation
        to a :class:`crowsetta.Annotation`.

        Returns
        -------
        annot : crowsetta.Annotation

        Examples
        --------
        >>> example = crowsetta.data.get('aud-bbox')
        >>> audacitybbox = crowsetta.formats.bbox.AudBBox.from_file(example.annot_path)
        >>> annot = audacitybbox.to_annot()
        """
        bboxes = self.to_bbox()
        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, bboxes=bboxes)

    def to_file(self, annot_path: PathLike) -> None:
        """Make a txt file from this annotation
        in extended label track format that can be read by Audacity.

        Parameters
        ----------
        annot_path : str, pathlib.Path
             Path including filename where file should be saved.
             Must have extension '.txt'
        """
        crowsetta.validation.validate_ext(annot_path, extension=self.ext)
        lines = df_to_lines(self.df)
        with pathlib.Path(annot_path).open("w") as fp:
            fp.writelines(lines)
