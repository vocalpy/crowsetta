"""Module with functions meant to handle
any simple sequence-like annotation format.

The annotations can be a csv or txt file;
the format should have 3 columns that represent
the onset and offset times in seconds
and the labels of the segments
in the annotated sequences.

The default is to assume
a comma-separated values file
with a header 'onset_s, offset_s, label',
but this can be modified
with keyword arguments.

This format also assumes that each annotation file
corresponds to one annotated source file,
i.e. a single audio or spectrogram file.
"""

import pathlib
from typing import ClassVar, Mapping, Optional

import attr
import numpy as np
import pandas as pd
import pandera.pandas
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike


class SimpleSeqSchema(pandera.pandas.DataFrameModel):
    """A :class:`pandera.pandas.DataFrameModel`
    that validates a :type:`pandas.DataFrame`
    loaded from a csv or txt file in a 'simple-seq' format.

    The :meth:`SimpleSeq.from_file` loads the :type:`pandas.DataFrame`
    and makes any changes needed to get it to this format
    before validation, e.g., changing column names.
    """

    onset_s: Optional[Series[float]] = pandera.pandas.Field()
    offset_s: Optional[Series[float]] = pandera.pandas.Field()
    label: Series[pd.StringDtype] = pandera.pandas.Field(coerce=True)

    class Config:
        ordered = True
        strict = True


SIMPLESEQ_COLUMNS = ("onset_s", "offset_s", "label")


@crowsetta.interface.SeqLike.register
@attr.define
class SimpleSeq:
    """Class meant to represent any simple sequence-like annotation format.

    The annotations can be a csv or txt file;
    the format should have 3 columns that represent
    the onset and offset times in seconds
    and the labels of the segments
    in the annotated sequences.

    The default is to assume
    a comma-separated values file
    with a header 'onset_s, offset_s, label',
    but this can be modified
    with keyword arguments.

    This format also assumes that each annotation file
    corresponds to one annotated source file,
    i.e. a single audio or spectrogram file.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'simple-seq'``.
    ext: str
        Extension of files in annotation format:
        ``('.csv', '.txt')``
    onsets_s : numpy.ndarray
        Vector of floats corresponding
        to beginning of segments, i.e. onsets, in seconds
    offsets_s : numpy.ndarray
        Vector of floats corresponding
        to ends of segments, i.e. offsets, in seconds
    labels : numpy.ndarray
        Vector of string labels for segments
    annot_path : str, pathlib.Path
        Path to file from which annotations were loaded.
    notated_path : str. pathlib.Path
        path to file that ``annot_path`` annotates.
        E.g., an audio file, or an array file
        that contains a spectrogram generated from audio.
        Optional, default is None.
    """

    name: ClassVar[str] = "simple-seq"
    ext: ClassVar[str] = (".csv", ".txt")

    onsets_s: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    offsets_s: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    labels: np.ndarray = attr.field(eq=attr.cmp_using(eq=np.array_equal))
    annot_path: pathlib.Path
    notated_path: Optional[pathlib.Path] = attr.field(default=None, converter=attr.converters.optional(pathlib.Path))

    @classmethod
    def from_file(
        cls,
        annot_path: PathLike,
        notated_path: Optional[PathLike] = None,
        columns_map: Optional[Mapping] = None,
        read_csv_kwargs: Optional[Mapping] = None,
        default_label: str = "-",
    ) -> "Self":  # noqa: F821
        """Load annotations from a file
        in the 'simple-seq' format.

        The annotations can be a csv or txt file;
        the format should have 3 columns that represent
        the onset and offset times in seconds
        and the labels of the segments
        in the annotated sequences.

        The default is to assume
        a comma-separated values file
        with a header 'onset_s, offset_s, label',
        but this can be modified
        with keyword arguments.

        This format also assumes that each annotation file
        corresponds to one annotated source file,
        i.e. a single audio or spectrogram file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to an annotation file,
            with one of the extensions {'.csv', '.txt'}.
        notated_path : str, pathlib.Path
            Path to file that ``annot_path`` annotates.
            E.g., an audio file, or an array file
            that contains a spectrogram generated from audio.
            Optional, default is None.
        columns_map : dict-like
            Maps column names in header of ``annot_path``
            to the standardized names
            used by this format.
            E.g., ``{'begin_time': 'onset_s', 'end_time': 'offset_s', 'text': 'label'}``.
            Optional, default is None--assumes that
            columns have the standardized names.
        read_csv_kwargs : dict
            Keyword arguments passed to
            :func:`pandas.read_csv`. Default is None,
            in which case all defaults for
            :func:`pandas.read_csv` will be used.

        Examples
        --------
        >>> path = crowsetta.example('bl26lb16', return_path=True)
        >>> simple = crowsetta.formats.seq.SimpleSeq.from_file(path,
        >>>                                                    columns_map={'start_seconds': 'onset_s',
        >>>                                                                 'stop_seconds': 'offset_s',
        >>>                                                                 'name': 'label'},
        >>>                                                    read_csv_kwargs={'index_col': 0})
        """
        annot_path = pathlib.Path(annot_path)
        crowsetta.validation.validate_ext(annot_path, extension=cls.ext)

        if read_csv_kwargs:
            df = pd.read_csv(annot_path, **read_csv_kwargs)
        else:
            df = pd.read_csv(annot_path)

        if len(df) == 0:
            # handle empty csv file, fixes https://github.com/vocalpy/crowsetta/issues/264
            return cls(
                onsets_s=[],
                offsets_s=[],
                labels=[],
                annot_path=annot_path,
                notated_path=notated_path,
            )

        if columns_map is not None:
            if not isinstance(columns_map, dict):
                raise TypeError(f"The `columns_map` argument must be a `dict` but type was: {type(dict)}")
            if not all((isinstance(k, str) and isinstance(v, str) for k, v in columns_map.items())):
                raise ValueError(
                    "The `columns_map` argument must be a dict that maps string keys to string values, "
                    "but not all keys and values were strings."
                )
            if not all(v in SIMPLESEQ_COLUMNS for v in columns_map.values()):
                invalid_values = [v for v in columns_map.values() if v not in SIMPLESEQ_COLUMNS]
                raise ValueError(
                    f"The `columns_map` argument must map keys (column names in the csv) "
                    'to these values: ("onset_s", "offset_s", "label"). '
                    f"The following values are invalid: {invalid_values}"
                )
            df.columns = [
                columns_map[column_name] if column_name in columns_map else column_name for column_name in df.columns
            ]

        if "label" not in df.columns:
            df["label"] = default_label

        if not all([col_name in df.columns for col_name in SIMPLESEQ_COLUMNS]):
            raise ValueError(
                "Annotations loaded from path did not have expected column names. "
                f"Column names from loaded csv file were: {df.columns.to_list()}\n"
                f"Expected column names are: {SIMPLESEQ_COLUMNS}\n"
                f"Please either re-map the column names using the `columns_map` argument, "
                "or if needed modify the csv file directly. "
                "Note that you only need to remap the column names that correspond to onset "
                "times, offset times, and labels; other columns will be ignored."
            )
        df = df[list(SIMPLESEQ_COLUMNS)]  # put in correct order
        df = SimpleSeqSchema.validate(df)

        return cls(
            onsets_s=df["onset_s"].values,
            offsets_s=df["offset_s"].values,
            labels=df["label"].values,
            annot_path=annot_path,
            notated_path=notated_path,
        )

    def to_seq(self, round_times: bool = True, decimals: int = 3) -> crowsetta.Sequence:
        """Convert this annotation to a :class:`crowsetta.Sequence`.

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
        seq : crowsetta.Sequence

        Examples
        --------
        >>> path = crowsetta.example('bl26lb16', return_path=True)
        >>> simple = crowsetta.formats.seq.SimpleSeq.from_file(path,
        >>>                                                    columns_map={'start_seconds': 'onset_s',
        >>>                                                                 'stop_seconds': 'offset_s',
        >>>                                                                 'name': 'label'},
        >>>                                                    read_csv_kwargs={'index_col': 0})
        >>> seq = simple.to_seq()

        Notes
        -----
        The ``round_times`` and ``decimals`` arguments are provided
        to reduce differences across platforms
        due to floating point error, e.g. when loading annotation files
        and then sending them to a csv file,
        the result should be the same on Windows and Linux.
        """
        if round_times:
            onsets_s = np.around(self.onsets_s, decimals=decimals)
            offsets_s = np.around(self.offsets_s, decimals=decimals)
        else:
            onsets_s = self.onsets_s
            offsets_s = self.offsets_s

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
        >>> path = crowsetta.example('bl26lb1b', return_path=True)
        >>> simple = crowsetta.formats.seq.SimpleSeq.from_file(path,
        >>>                                                    columns_map={'start_seconds': 'onset_s',
        >>>                                                                 'stop_seconds': 'offset_s',
        >>>                                                                 'name': 'label'},
        >>>                                                    read_csv_kwargs={'index_col': 0})
        >>> annot = simple.to_annot()

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

    def to_file(self, annot_path: PathLike, to_csv_kwargs: Optional[Mapping] = None) -> None:
        """Save this 'simple-seq' annotation to a csv file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path with filename of csv file that should be saved
        to_csv_kwargs : dict-like
            keyword arguments passed to
            :meth:`pandas.DataFrame.to_csv`.
            Default is None, in which case
            defaults for :func:`pandas.to_csv`
            will be used, except ``index``
            is set to False.
        """
        df = pd.DataFrame.from_records({"onset_s": self.onsets_s, "offset_s": self.offsets_s, "label": self.labels})
        df = df[["onset_s", "offset_s", "label"]]  # put in correct order
        try:
            df = SimpleSeqSchema.validate(df)
        except pandera.errors.SchemaError as e:
            raise ValueError(f"Annotations produced an invalid dataframe, cannot convert to csv:\n{df}") from e
        if to_csv_kwargs:
            df.to_csv(annot_path, **to_csv_kwargs)
        else:
            df.to_csv(annot_path, index=False)
