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


class AudBBoxSchema(pandera.DataFrameModel):
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


    Examples
    --------
    >>> audbbox = crowsetta.example('spinetail.txt')
    >>> print(audbbox)
    AudBBox(df=    begin_time_s  end_time_s label  low_freq_hz  high_freq_hz
    0       0.101385    0.367520    SP  6441.064453  12296.577148
    1       0.506924    3.041545  CRER  2593.156006   8866.920898
    2       1.203945    1.482753    SP  6608.365234  11543.726562
    3       2.724718    3.218969    SP  4851.710938  12631.178711
    4       5.221319    7.869998  CRER  2509.505615   8699.620117
    5       6.260514    6.666053    SP  5939.163574  12798.478516
    6       7.946037    8.288210    SP  4600.760254  13049.430664
    7       8.896519    9.302059    SP  5827.929351  12513.294481
    8       9.973733   10.353927    SP  4851.710938  13969.581055
    9      11.329756   13.750319  CRER  2091.254639   9117.871094
    10     11.773314   12.077469    SP  6106.464355  12296.577148
    11     12.660432   12.939240    SP  5604.562500  12296.577148
    12     15.435842   15.879400    SP  4015.209229  13216.730469
    13     16.170882   16.563748    SP  4098.859375  12463.878906
    14     16.437017   18.730849  CRER  2676.806152   8699.620117
    15     17.159384   17.514231    SP  5688.213379  12714.829102
    16     18.198578   18.502733    SP  5353.612305  12463.878906
    17     19.073023   19.465889    SP  4349.810059  12296.577148, annot_path=PosixPath('/Users/davidnicholson/Documents/repos/vocalpy/crowsetta/src/crowsetta/examples/spinetail.txt'), audio_path=None)  # noqa: E501
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
        >>> path = crowsetta.example('spinetail.txt', return_path=True)
        >>> audbbox = crowsetta.formats.bbox.AudBBox.from_file(path)
        >>> print(audbbox)
        AudBBox(df=    begin_time_s  end_time_s label  low_freq_hz  high_freq_hz
        0       0.101385    0.367520    SP  6441.064453  12296.577148
        1       0.506924    3.041545  CRER  2593.156006   8866.920898
        2       1.203945    1.482753    SP  6608.365234  11543.726562
        3       2.724718    3.218969    SP  4851.710938  12631.178711
        4       5.221319    7.869998  CRER  2509.505615   8699.620117
        5       6.260514    6.666053    SP  5939.163574  12798.478516
        6       7.946037    8.288210    SP  4600.760254  13049.430664
        7       8.896519    9.302059    SP  5827.929351  12513.294481
        8       9.973733   10.353927    SP  4851.710938  13969.581055
        9      11.329756   13.750319  CRER  2091.254639   9117.871094
        10     11.773314   12.077469    SP  6106.464355  12296.577148
        11     12.660432   12.939240    SP  5604.562500  12296.577148
        12     15.435842   15.879400    SP  4015.209229  13216.730469
        13     16.170882   16.563748    SP  4098.859375  12463.878906
        14     16.437017   18.730849  CRER  2676.806152   8699.620117
        15     17.159384   17.514231    SP  5688.213379  12714.829102
        16     18.198578   18.502733    SP  5353.612305  12463.878906
        17     19.073023   19.465889    SP  4349.810059  12296.577148, annot_path=PosixPath('/Users/davidnicholson/Documents/repos/vocalpy/crowsetta/src/crowsetta/examples/spinetail.txt'), audio_path=None)  # noqa: E501
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
        >>> path = crowsetta.example('spinetail.txt', return_path=True)
        >>> audbbox = crowsetta.formats.bbox.AudBBox.from_file(path)
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
        >>> path = crowsetta.example('spinetail.txt', return_path=True)
        >>> audbbox = crowsetta.formats.bbox.AudBBox.from_file(path)
        >>> annot = audbbox.to_annot()
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
