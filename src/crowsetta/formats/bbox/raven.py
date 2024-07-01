"""module with functions that handle .txt annotation files
from Raven (https://ravensoundsoftware.com/software/).

Adapted in part from ``opensoundscape``
https://github.com/kitzeslab/opensoundscape/blob/master/opensoundscape/annotations.py
under MIT license
"""
import pathlib
from typing import ClassVar, List, Optional

import attr
import pandas as pd
import pandera
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike


class RavenSchema(pandera.DataFrameModel

):
    """A :class:`pandera.DataFrameModel

` that validates :type:`pandas.DataFrame`s
    loaded from a txt file, created by exporting a Selection Table
    from Raven.
    """

    begin_time_s: Series[float] = pandera.Field()
    end_time_s: Series[float] = pandera.Field()
    low_freq_hz: Series[float] = pandera.Field()
    high_freq_hz: Series[float] = pandera.Field()
    annotation: Series[pd.StringDtype] = pandera.Field(coerce=True)

    class Config:
        # we set strict fo False
        # because we just ignore other columns, e.g. 'Selection',
        # and because there should be an annotation column
        # and we don't want to throw an error because of it
        strict = False


@crowsetta.interface.BBoxLike.register
@attr.define
class Raven:
    """Class that represents txt annotation files
    from Raven (https://ravensoundsoftware.com/software/),
    created by exporting a Selection Table.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: 'raven'.
    ext: str
        Extension of files in annotation format: '.txt'
    df : pandas.DataFrame
        with annotations loaded into it
    annot_path : str, pathlib.Path
        Path to Raven txt file from which annotations were loaded.
    audio_path : str. pathlib.Path
        Path to audio file that the Raven txt file annotates.
    """

    name: ClassVar[str] = "raven"
    ext: ClassVar[str] = (".txt",)
    COLUMNS_MAP: ClassVar[dict] = {
        "Begin Time (s)": "begin_time_s",
        "End Time (s)": "end_time_s",
        "Low Freq (Hz)": "low_freq_hz",
        "High Freq (Hz)": "high_freq_hz",
    }

    df: pd.DataFrame
    annot_path: pathlib.Path
    annot_col: str
    audio_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls, annot_path: PathLike, annot_col: str = "Annotation", audio_path: Optional[PathLike] = None
    ) -> "Self":  # noqa: F821
        """Load annotations from a Raven annotation file,
        created by exporting a Selection Table.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to a txt file exported from Raven.
        annot_col : str
            Name of column that contains annotations.
        audio_path : str, pathlib.Path
            Path to audio file that the Raven txt file annotates.
            Optional, defaults to None.

        Examples
        --------
        >>> example = crowsetta.data.get('raven')
        >>> raven = crowsetta.formats.bbox.Raven.from_file(example.annot_path)
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        #  assume file is space-separated with no header
        df = pd.read_csv(annot_path, sep="\t")
        if len(df) < 1:
            raise ValueError(f"Cannot load annotations, " f"there are no rows in Raven txt file:\n{df}")
        columns_map = dict(cls.COLUMNS_MAP)  # copy
        columns_map.update({annot_col: "annotation"})
        df.rename(columns=columns_map, inplace=True)
        df = RavenSchema.validate(df)

        return cls(
            df=df,
            annot_path=annot_path,
            annot_col=annot_col,
            audio_path=audio_path,
        )

    def to_bbox(self) -> List[crowsetta.BBox]:
        """Convert this Raven annotation to a
        :class:`list` of :class:`crowsetta.Bbox` instances.

        Returns
        -------
        bboxes : list
            A :class:`list` of :class:`crowsetta.BBox` instances.

        Examples
        --------
        >>> example = crowsetta.data.get('raven')
        >>> raven = crowsetta.formats.bbox.Raven.from_file(example.annot_path)
        >>> bboxes = raven.to_bbox()
        """
        bboxes = []
        for begin_time, end_time, low_freq, high_freq, label in zip(
            self.df.begin_time_s.values,
            self.df.end_time_s.values,
            self.df.low_freq_hz.values,
            self.df.high_freq_hz.values,
            self.df["annotation"].values,
        ):
            bboxes.append(
                crowsetta.BBox(onset=begin_time, offset=end_time, low_freq=low_freq, high_freq=high_freq, label=label)
            )
        return bboxes

    def to_annot(self) -> crowsetta.Annotation:
        """Convert this Raven annotation to a
        :class:`crowsetta.Annotation`.

        Returns
        -------
        annot : crowsetta.Annotation

        Examples
        --------
        >>> example = crowsetta.data.get('raven')
        >>> raven = crowsetta.formats.bbox.Raven.from_file(example.annot_path)
        >>> annot = raven.to_annot()
        """
        bboxes = self.to_bbox()
        return crowsetta.Annotation(annot_path=self.annot_path, notated_path=self.audio_path, bboxes=bboxes)

    def to_file(self, annot_path: PathLike) -> None:
        """Make a txt file that can be read by Raven
        from this annotation

        Parameters
        ----------
        annot_path : str, pahtlib.Path
             Path including filename where file should be saved.
             Must have extension '.txt'
        """
        crowsetta.validation.validate_ext(annot_path, extension=self.ext)

        columns_map = {v: k for k, v in self.COLUMNS_MAP.items()}  # copy
        columns_map.update({"annotation": self.annot_col})
        df_out = self.df.rename(columns=columns_map)
        df_out.to_csv(annot_path, sep="\t", index=False)
