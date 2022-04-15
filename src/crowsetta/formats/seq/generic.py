"""
generic format,
meant to be an abstraction of
any sequence-like format.

Consists of ``Annotation``s,
each with a ``Sequence`` made up
of ``Segment``s.

Functions in this module
load the format from a .csv,
or write a .csv in the generic format.
Other formats that convert to ``Annotation``s
with ``Sequence``s can be converted
to this format.
"""
import os
from collections import OrderedDict

from typing import ClassVar, List, Optional, Union

import attr
import pandas as pd
import pandera
from pandera.typing import Series

import crowsetta
from crowsetta.typing import PathLike


ONSET_OFFSET_COLS_ERR = """For onset times and offset times, 
all values must be specified in at least one unit: 
seconds (float), or sample number (integer). All rows must be non-null for either 
'onset_s' and 'offset_s' or 'onset_ind' and 'offset_ind'.
Both units can also be specified. Conversion between units is not validated.
"""


class GenericSeqSchema(pandera.SchemaModel):
    """``pandera.SchemaModel`` that validates ``pandas`` dataframes
    loaded from a .csv file  in the ``'generic-seq'`` annotation
    format.
    """
    label: Series[pd.StringDtype] = pandera.Field(coerce=True)
    onset_s: Optional[Series[float]] = pandera.Field()
    offset_s: Optional[Series[float]] = pandera.Field()
    onset_ind: Optional[Series[int]] = pandera.Field()
    offset_ind: Optional[Series[int]] = pandera.Field()

    audio_path: Series[str] = pandera.Field()
    annot_path: Series[str] = pandera.Field()
    sequence: Series[int] = pandera.Field()
    annotation: Series[int] = pandera.Field()

    @pandera.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def both_onset_s_and_offset_s_if_either(cls, df: pd.DataFrame) -> bool:
        """check that, if one of {'onset_s', 'offset_s'} column is present,
        then both are present"""
        if any([col in df for col in ('onset_s', 'offset_s')]):
            return all([col in df for col in ('onset_s', 'offset_s')])
        else:
            return True

    @pandera.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def both_onset_ind_and_offset_ind_if_either(cls, df: pd.DataFrame) -> bool:
        """check that, if one of {'onset_ind', 'offset_ind'} column is present,
        then both are present"""
        if any([col in df for col in ('onset_ind', 'offset_ind')]):
            return all([col in df for col in ('onset_ind', 'offset_ind')])
        else:
            return True

    @pandera.dataframe_check(error=ONSET_OFFSET_COLS_ERR)
    def onset_offset_s_and_ind_are_not_both_missing(cls, df: pd.DataFrame) -> bool:
        """check that at least one of the on/offset column pairs is present:
        either {'onset_s', 'offset_s'} or {'onset_ind', 'offset_ind'}"""
        if 'onset_s' not in df and 'offset_s' not in df:
            return 'onset_ind' in df and 'offset_ind' in df
        elif 'onset_ind' not in df and 'offset_ind' not in df:
            return 'onset_s' in df and 'offset_s' in df
        elif all([col in df for col in ('onset_s', 'offset_s', 'onset_ind', 'offset_ind')]):
            #  i.e., else return True, but extra verbose for clarity
            return True

    class Config:
        ordered = True
        strict = True


def annot2csv(annot: Union[crowsetta.Annotation, List[crowsetta.Annotation]],
              csv_path: PathLike,
              abspath: bool = False,
              basename: bool = False) -> None:
    """write sequence-like ``crowsetta.Annotation``
    to a .csv file in the ``'generic-seq'`` format

    Parameters
    ----------
    annot : crowsetta.Annotation, or list of Annotations
    csv_path : str, pathlib.Path
        path including filename of .csv to write to,
        will be created (or overwritten if it exists already)
    abspath : bool
        if True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        if True, discard any information about path and just use file name.
        Default is False.

    Notes
    -----
    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful when working with multiple copies of files, and for
    reproducibility (so you know which copy of a file you were working with).
    Default for both is False, in which case the filename is saved just as it is passed to
    this function in a Sequence object.
    """
    if not (isinstance(annot, crowsetta.Annotation) or isinstance(annot, list)):
        raise TypeError('annot must be Annotation or list of Annotations, '
                        f'not type {type(annot)})')

    if isinstance(annot, crowsetta.Annotation):
        # put in a list so we can iterate over it
        annot = [annot]

    if not all([isinstance(annot_, crowsetta.Annotation) for annot_ in annot]):
        raise TypeError('not all objects in annot are of type Annotation')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    records = []
    for annot_num, annot_ in enumerate(annot):
        seq_list = [annot_.seq]
        for seq_num, seq in enumerate(seq_list):
            for segment in seq.segments:
                row = OrderedDict({
                    key: val
                    for key, val in segment.asdict().items()
                    # don't keep onset or offset if they are None
                    # but keep any other Nones, so those other Nones will raise expected errors downstreams
                    if not(val is None and any([key.startswith(prefix) for prefix in ('onset', 'offset')]))
                })  # OrderedDict is default; being extra explicit here
                annot_path = annot_.annot_path
                audio_path = annot_.audio_path
                if abspath:
                    annot_path = os.path.abspath(annot_path)
                    if audio_path is not None:
                        audio_path = os.path.abspath(audio_path)
                elif basename:
                    annot_path = os.path.basename(annot_path)
                    if audio_path is not None:
                        audio_path = os.path.basename(audio_path)
                # need to put in audio_path before annot_path
                if audio_path is not None:
                    row['audio_path'] = audio_path
                else:
                    row['audio_path'] = 'None'
                row['annot_path'] = annot_path
                # we use 'sequence' and 'annotation' fields when we are
                # loading back into Annotations
                row['sequence'] = seq_num
                row['annotation'] = annot_num
                records.append(row)

    df = pd.DataFrame.from_records(records)
    GenericSeqSchema.validate(df)
    df.to_csv(csv_path, index=False)


def csv2annot(csv_path: PathLike) -> List[crowsetta.Annotation]:
    """loads a comma-separated values (csv) file containing annotations
    for song files, returns contents as a list of Annotation objects

    Parameters
    ----------
    csv_path : str, pathlib.Path
        Path to .csv file containing annotations
        saved in the ``'generic-seq'`` format.

    Returns
    -------
    annot_list : list
        list of Annotations
    """
    df = pd.read_csv(csv_path)
    GenericSeqSchema.validate(df)

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
                f"found multiple values for 'annot_path' for annotation #{annotation_ind}:"
                f"\n{annot_path}"
            )
        annot_path = annot_path[0]
        # 2. audio_path
        audio_path = df_annot.audio_path.unique()
        if len(audio_path) > 1:
            raise ValueError(
                f"found multiple values for 'audio_path' for annotation #{annotation_ind}:"
                f"\n{audio_path}"
            )
        audio_path = audio_path[0]
        # 3. Sequence
        seq_uniq = df_annot.sequence.unique()
        assert len(seq_uniq) > 0
        if len(seq_uniq) > 1:
            raise ValueError(
                'Multiple sequences per annotation are not implemented'
            )
        labels = df_annot.label.values
        if 'onset_s' and 'offset_s' in df_annot:
            onsets_s = df_annot.onset_s.values
            offsets_s = df_annot.offset_s.values
        else:
            onsets_s = None
            offsets_s = None
        if 'onset_ind' and 'offset_ind' in df_annot:
            onsets_inds = df_annot.onset_ind.values
            offsets_inds = df_annot.offset_ind.values
        else:
            onsets_inds = None
            offsets_inds = None
        seq = crowsetta.Sequence.from_keyword(
            labels=labels,
            onsets_s=onsets_s,
            offsets_s=offsets_s,
            onset_inds=onsets_inds,
            offset_inds=offsets_inds,
        )
        annot = crowsetta.Annotation(
            annot_path=annot_path,
            audio_path=audio_path,
            seq=seq
        )
        annot_list.append(annot)

    return annot_list


@crowsetta.interface.SeqLike.register
@attr.define
class GenericSeq:
    """
    class that represents annotations from a generic format,
    meant to be an abstraction of
    any sequence-like format.

    Consists of ``Annotation``s,
    each with a ``Sequence`` made up
    of ``Segment``s.

    Other formats that convert to ``Annotation``s
    with ``Sequence``s can be converted
    to this format.

    Attributes
    ----------
    name: str
        shorthand name for annotation format: ``'generic-seq'``
    ext: str
        extension of files in annotation format: ``'.csv'``
    annots : list
        of ``crowsetta.Annotation`` instances
    """
    name: ClassVar[str] = 'generic-seq'
    ext: ClassVar[str] = '.csv'

    annots: List[crowsetta.Annotation]

    @classmethod
    def from_file(cls,
                  csv_path: PathLike) -> 'Self':
        """load annotations in 'generic-seq' format from a .csv file

        Parameters
        ----------
        csv_path : str, pathlib.Path
            Path to .csv file containing annotations
            saved in the ``'generic-seq'`` format.
            """
        annots = csv2annot(csv_path=csv_path)
        return cls(annots=annots)

    def to_annot(self) -> List[crowsetta.Annotation]:
        """returns these ``crowsetta.Annotation`` instances
         as a list

         This is the same as accessing the list of ``Annotation``
         instances directly. It is implemented so that this class
         conforms with the ``SeqLike`` interface.
         """
        return self.annots

    def to_seq(self) -> List[crowsetta.Sequence]:
        """return a list of ``crowsetta.Sequence``,
        one for every annotation"""
        return [annot.seq for annot in self.annots]

    def to_file(self,
                csv_path: PathLike,
                abspath: bool = False,
                basename: bool = False) -> None:
        """writes these annotations to a .csv file
        in ``'generic-seq'`` format.

        Parameters
        ----------
        csv_path : str, pathlib.Path
            path including filename of .csv to write to,
            will be created (or overwritten if it exists already)
        abspath : bool
            if True, converts filename for each audio file into absolute path.
            Default is False.
        basename : bool
            if True, discard any information about path and just use file name.
            Default is False.
        """
        annot2csv(csv_path=csv_path,
                  annot=self.annots,
                  abspath=abspath,
                  basename=basename)