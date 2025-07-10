"""
Generic sequence format,
meant to be an abstraction of
any sequence-like format.

Consists of :class:`crowsetta.Annotation`
instances, each with a :class:`crowsetta.Sequence`
made up of :class:`crowsetta.Segment`s.

Functions in this module
load the format from a csv file,
or write a csv file in the generic format.
Other formats that convert to
:class:`~crowsetta.Annotation`s
with :class:`~crowsetta.Sequence`s can be converted
to this format.
"""

import os
from collections import OrderedDict
from typing import ClassVar, List, Optional, Union

import attr
import pandas as pd
import pandera.pandas
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike

ONSET_OFFSET_COLS_ERR = """For onset times and offset times,
all values must be specified in at least one unit:
seconds (float), or sample number (integer). All rows must be non-null for either
'onset_s' and 'offset_s' or 'onset_sample' and 'offset_sample'.
Both units can also be specified. Conversion between units is not validated.
"""


class GenericSeqSchema(pandera.pandas.DataFrameModel):
    """A :class: `pandera.pandas.DataFrameModel` that validates
    a :type:`pandas.DataFrame` loaded from a csv file
    in the ``'generic-seq'`` annotation format.
    """

    label: Series[pd.StringDtype] = pandera.pandas.Field(coerce=True)
    onset_s: Optional[Series[float]] = pandera.pandas.Field()
    offset_s: Optional[Series[float]] = pandera.pandas.Field()
    onset_sample: Optional[Series[int]] = pandera.pandas.Field()
    offset_sample: Optional[Series[int]] = pandera.pandas.Field()

    notated_path: Series[str] = pandera.pandas.Field(coerce=True)
    annot_path: Series[str] = pandera.pandas.Field(coerce=True)
    sequence: Series[int] = pandera.pandas.Field()
    annotation: Series[int] = pandera.pandas.Field()

    @pandera.pandas.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def both_onset_s_and_offset_s_if_either(cls, df: pd.DataFrame) -> bool:
        """check that, if one of {'onset_s', 'offset_s'} column is present,
        then both are present"""
        if any([col in df for col in ("onset_s", "offset_s")]):
            return all([col in df for col in ("onset_s", "offset_s")])
        else:
            return True

    @pandera.pandas.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def both_onset_sample_and_offset_sample_if_either(cls, df: pd.DataFrame) -> bool:
        """check that, if one of {'onset_sample', 'offset_sample'} column is present,
        then both are present"""
        if any([col in df for col in ("onset_sample", "offset_sample")]):
            return all([col in df for col in ("onset_sample", "offset_sample")])
        else:
            return True

    @pandera.pandas.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def onset_offset_s_and_ind_are_not_both_missing(cls, df: pd.DataFrame) -> bool:
        """check that at least one of the on/offset column pairs is present:
        either {'onset_s', 'offset_s'} or {'onset_sample', 'offset_sample'}"""
        if "onset_s" not in df and "offset_s" not in df:
            return "onset_sample" in df and "offset_sample" in df
        elif "onset_sample" not in df and "offset_sample" not in df:
            return "onset_s" in df and "offset_s" in df
        elif all([col in df for col in ("onset_s", "offset_s", "onset_sample", "offset_sample")]):
            #  i.e., else return True, but extra verbose for clarity
            return True

    class Config:
        ordered = True
        strict = True


def annot2df(
    annot: Union[crowsetta.Annotation, List[crowsetta.Annotation]], abspath: bool = False, basename: bool = False
) -> pd.DataFrame:
    """Convert sequence-like :class:`crowsetta.Annotation`
    to a :type:`pandas.DataFrame` in the ``'generic-seq'`` format.

    Parameters
    ----------
    annot : crowsetta.Annotation, or list of Annotations
    csv_path : str, pathlib.Path
        Path including filename of csv file to write to,
        will be created (or overwritten if it exists already)
    abspath : bool
        If True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        If True, discard any information about path and just use file name.
        Default is False.

    Notes
    -----
    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful when working with multiple copies of files, and for
    reproducibility (so you know which copy of a file you were working with).
    Default for both is False, in which case the filename is saved just as it is passed to
    this function in a :class:`crowsetta.Sequence` object.
    """
    if not (isinstance(annot, crowsetta.Annotation) or isinstance(annot, list)):
        raise TypeError("annot must be Annotation or list of Annotations, " f"not type {type(annot)})")

    if isinstance(annot, crowsetta.Annotation):
        # put in a list so we can iterate over it
        annot = [annot]

    if not all([isinstance(annot_, crowsetta.Annotation) for annot_ in annot]):
        raise TypeError("not all objects in annot are of type Annotation")

    if abspath and basename:
        raise ValueError(
            "abspath and basename arguments cannot both be set to True, "
            "unclear whether absolute path should be saved or if no path "
            "information (just base filename) should be saved."
        )

    records = []
    for annot_num, annot_ in enumerate(annot):
        if isinstance(annot_.seq, crowsetta.Sequence):
            seq_list = [annot_.seq]
        elif isinstance(annot_.seq, list):
            seq_list = annot_.seq
        for seq_num, seq in enumerate(seq_list):
            for segment in seq.segments:
                row = OrderedDict(
                    {
                        key: val
                        for key, val in segment.asdict().items()
                        # don't keep onset or offset if they are None
                        # but keep any other Nones, so those other Nones will raise expected errors downstreams
                        if not (val is None and any([key.startswith(prefix) for prefix in ("onset", "offset")]))
                    }
                )  # OrderedDict is default; being extra explicit here
                annot_path = annot_.annot_path
                notated_path = annot_.notated_path
                if abspath:
                    annot_path = os.path.abspath(annot_path)
                    if notated_path is not None:
                        notated_path = os.path.abspath(notated_path)
                elif basename:
                    annot_path = os.path.basename(annot_path)
                    if notated_path is not None:
                        notated_path = os.path.basename(notated_path)
                # need to put in notated_path before annot_path
                if notated_path is not None:
                    row["notated_path"] = notated_path
                else:
                    row["notated_path"] = "None"
                row["annot_path"] = annot_path
                # we use 'sequence' and 'annotation' fields when we are
                # loading back into Annotations
                row["sequence"] = seq_num
                row["annotation"] = annot_num
                records.append(row)

    df = pd.DataFrame.from_records(records)
    df = GenericSeqSchema.validate(df)
    return df


def annot2csv(
    annot: Union[crowsetta.Annotation, List[crowsetta.Annotation]],
    csv_path: PathLike,
    abspath: bool = False,
    basename: bool = False,
) -> None:
    """Write sequence-like :class:`crowsetta.Annotation`
    to a csv file in the ``'generic-seq'`` format

    Parameters
    ----------
    annot : crowsetta.Annotation, or list of Annotations
    csv_path : str, pathlib.Path
        Path including filename of csv file to write to,
        will be created (or overwritten if it exists already)
    abspath : bool
        If True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        If True, discard any information about path and just use file name.
        Default is False.

    Notes
    -----
    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful when working with multiple copies of files, and for
    reproducibility (so you know which copy of a file you were working with).
    Default for both is False, in which case the filename is saved just as it is passed to
    this function in a Sequence object.
    """
    df = annot2df(annot, abspath, basename)
    df.to_csv(csv_path, index=False)


def csv2annot(csv_path: PathLike) -> List[crowsetta.Annotation]:
    """Loads a comma-separated values (csv) file containing annotations
    for song files, returns contents as a
    :class:`list` of :class:`crowsetta.Annotation` instances.

    Parameters
    ----------
    csv_path : str, pathlib.Path
        Path to csv file containing annotations
        saved in the ``'generic-seq'`` format.

    Returns
    -------
    annot_list : list
        A :class:`list` of :class:`crowsetta.Annotation` instances.
    """
    df = pd.read_csv(csv_path)
    df = GenericSeqSchema.validate(df)

    annot_list = []
    # tried doing this various ways with `pandas.DataFrame.groupby('annotation')`
    # but they are all less readable +
    # required more work to convert -> `crowsetta.Annotation` instances
    for annotation_ind in df.annotation.unique():
        df_annot = df[df.annotation == annotation_ind]
        # ---- get what we need to build an Annotation instance
        # 1. annot_path
        annot_path = df_annot.annot_path.unique()
        if len(annot_path) > 1:
            raise ValueError(
                f"found multiple values for 'annot_path' for annotation #{annotation_ind}:" f"\n{annot_path}"
            )
        annot_path = annot_path[0]
        # 2. notated_path
        notated_path = df_annot.notated_path.unique()
        if len(notated_path) > 1:
            raise ValueError(
                f"found multiple values for 'notated_path' for annotation #{annotation_ind}:" f"\n{notated_path}"
            )
        notated_path = notated_path[0]
        # 3. Sequence
        seq_uniq = df_annot.sequence.unique()
        assert len(seq_uniq) > 0
        if len(seq_uniq) > 1:
            raise ValueError("Multiple sequences per annotation are not implemented")
        labels = df_annot.label.values
        if "onset_s" and "offset_s" in df_annot:
            onsets_s = df_annot.onset_s.values
            offsets_s = df_annot.offset_s.values
        else:
            onsets_s = None
            offsets_s = None
        if "onset_sample" and "offset_sample" in df_annot:
            onsets_inds = df_annot.onset_sample.values
            offsets_inds = df_annot.offset_sample.values
        else:
            onsets_inds = None
            offsets_inds = None
        seq = crowsetta.Sequence.from_keyword(
            labels=labels,
            onsets_s=onsets_s,
            offsets_s=offsets_s,
            onset_samples=onsets_inds,
            offset_samples=offsets_inds,
        )
        annot = crowsetta.Annotation(annot_path=annot_path, notated_path=notated_path, seq=seq)
        annot_list.append(annot)

    return annot_list


@crowsetta.interface.SeqLike.register
@attr.define
class GenericSeq:
    """Class that represents annotations from a generic format,
    meant to be an abstraction of
    any sequence-like format.

    Consists of :class:`crowsetta.Annotation`s,
    each with a :class:`crowsetta.Sequence` made up
    of :class:`crowsetta.Segment`s.

    Other formats that convert to :class:`~crowsetta.Annotation`s
    with :class:`~crowsetta.Sequence`s can be converted
    to this format.

    Attributes
    ----------
    name: str
        Shorthand name for annotation format: ``'generic-seq'``
    ext: str
        Extension of files in annotation format: ``'.csv'``
    annots : list
        A :class:`list` of :class:`crowsetta.Annotation` instances.
    """

    name: ClassVar[str] = "generic-seq"
    ext: ClassVar[str] = ".csv"

    annots: List[crowsetta.Annotation]

    @classmethod
    def from_file(cls, annot_path: PathLike) -> "Self":  # noqa: F821
        """Load annotations in 'generic-seq' format from a csv file.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path to csv file containing annotations
            saved in the ``'generic-seq'`` format.

        Examples
        --------
        >>> path = crowsetta.example('bird1.csv', return_path=True)
        >>> generic = crowsetta.formats.seq.GenericSeq.from_file(path)
        """
        annots = csv2annot(csv_path=annot_path)
        return cls(annots=annots)

    def to_seq(self) -> List[crowsetta.Sequence]:
        """Return a :class:`list` of :class:`crowsetta.Sequence` instances,
        one for every annotation.

        Examples
        --------
        >>> path = crowsetta.example('bird1.csv', return_path=True)
        >>> generic = crowsetta.formats.seq.GenericSeq.from_file(path)
        >>> seqs = generic.to_seq()
        """
        return [annot.seq for annot in self.annots]

    def to_annot(self) -> List[crowsetta.Annotation]:
        """Returns this set of :class:`crowsetta.Annotation` instances
        as a :class:`list`.

        This is the same as accessing the :class:`list` of :class:`crowsetta.Annotation`
        instances directly. The method is implemented so that this class
        conforms with the :class:`crowsetta.interface.seq.SeqLike` interface.

        Examples
        --------
        >>> path = crowsetta.example('bird1.csv', return_path=True)
        >>> generic = crowsetta.formats.seq.GenericSeq.from_file(path)
        >>> annots = generic.to_annot()
        """
        return self.annots

    def to_df(self, abspath: bool = False, basename: bool = False) -> pd.DataFrame:
        """Convert these annotations to a :type:`pandas.DataFrame`.

        abspath : bool
            If True, converts filename for each audio file into absolute path.
            Default is False.
        basename : bool
            If True, discard any information about path and just use file name.
            Default is False.
        """
        return annot2df(self.annots, abspath, basename)

    def to_file(self, annot_path: PathLike, abspath: bool = False, basename: bool = False) -> None:
        """Write these annotations to a csv file
        in ``'generic-seq'`` format.

        Parameters
        ----------
        annot_path : str, pathlib.Path
            Path including filename of csv file to write to,
            will be created (or overwritten if it exists already)
        abspath : bool
            If True, converts filename for each audio file into absolute path.
            Default is False.
        basename : bool
            If True, discard any information about path and just use file name.
            Default is False.
        """
        annot2csv(csv_path=annot_path, annot=self.annots, abspath=abspath, basename=basename)
