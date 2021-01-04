"""module for loading Praat TextGrid files into Annotations

uses the Python library textgrid
https://github.com/kylebgorman/textgrid
a version is distributed with this code (../textgrid) under MIT license
https://github.com/kylebgorman/textgrid/blob/master/LICENSE
"""
import os

import numpy as np
from textgrid import TextGrid, IntervalTier

from .annotation import Annotation
from .csv import annot2csv
from .meta import Meta
from .sequence import Sequence
from .validation import _parse_file


def textgrid2annot(annot_path,
                   abspath=False,
                   basename=False,
                   round_times=True,
                   decimals=3,
                   intervaltier_ind=0,
                   audio_ext='wav',
                   ):
    """convert Praat Textgrid file(s) into Annotation(s)

    Parameters
    ----------
    annot_path : str, Path
        filename of a .TextGrid annotation file, created by Praat.
    abspath : bool
        if True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        if True, discard any information about path and just use file name.
        Default is False.
    round_times : bool
        if True, round onsets_s and offsets_s.
        Default is True.
    decimals : int
        number of decimals places to round floating point numbers to.
        Only meaningful if round_times is True.
        Default is 3, so that times are rounded to milliseconds.
    intervaltier_ind : int
        index of IntervalTier in TextGrid file from which annotations
        should be taken. Default it 0, i.e. the first IntervalTier.
        Necessary in cases where files have multiple IntervalTiers.
        Currently there is only support for converting a single IntervalTier
        to a single Sequence.
    audio_ext : str
        extension of audio file associated with TextGrid file. Used to
        determine the filename of the audio file associated with the
        TextGrid file. Default is 'wav'.

    Returns
    -------
    annot : crowsetta.Annotation or list of Annotations
        each Interval in the first IntervalTier in a TextGrid file
        will become one segment in a sequence.
    """
    annot_path = _parse_file(annot_path, extension='.TextGrid')
    annots = []
    for a_textgrid in annot_path:
        tg = TextGrid.fromFile(a_textgrid)

        intv_tier = tg[intervaltier_ind]
        if type(intv_tier) != IntervalTier:
            raise ValueError(f'Index specified for IntervalTier was {intervaltier_ind}, '
                             f'but type at that index was {type(intv_tier)}, not an IntervalTier')

        audio_pathname = a_textgrid.replace('TextGrid', audio_ext)
        if abspath:
            audio_pathname = os.path.abspath(audio_pathname)
        elif basename:
            audio_pathname = os.path.basename(audio_pathname)

        intv_tier = tg[0]
        onsets_s = []
        offsets_s = []
        labels = []

        for interval in intv_tier:
            labels.append(interval.mark)
            onsets_s.append(interval.minTime)
            offsets_s.append(interval.maxTime)

        labels = np.asarray(labels)
        onsets_s = np.asarray(onsets_s)
        offsets_s = np.asarray(offsets_s)

        # do this *after* converting onsets_s and offsets_s to onsets_Hz and offsets_Hz
        # probably doesn't matter but why introduce more noise?
        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        # TODO: check for multiple sequences
        textgrid_seq = Sequence.from_keyword(labels=labels,
                                             onsets_s=onsets_s,
                                             offsets_s=offsets_s)
        annot = Annotation(annot_path=a_textgrid,
                           audio_path=audio_pathname,
                           seq=textgrid_seq)
        annots.append(annot)

    if len(annots) == 1:
        return annots[0]
    else:
        return annots


def textgrid2csv(annot_path, csv_filename, abspath=False, basename=False):
    """saves annotation from TextGrid file(s) in a comma-separated values
    (csv) file, where each row represents one syllable from one
    .not.mat file.

    Parameters
    ----------
    annot_path : str, Path, or list
        if list, list of strings or Path objects pointing to TextGrid files
    csv_filename : str
        name for csv file that is created

    The following two parameters specify how file names for audio files are saved. These
    options are useful for working with multiple copies of files and for reproducibility.
    Default for both is False, in which case the filename is saved just as it is passed to
    this function.
    abspath : bool
        if True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        if True, discard any information about path and just use file name.
        Default is False.

    Returns
    -------
    None
    """
    annot_path = _parse_file(annot_path, extension='.TextGrid')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annots = textgrid2annot(annot_path)
    annot2csv(annots, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='textgrid',
    ext='TextGrid',
    from_file=textgrid2annot,
    to_csv=textgrid2csv,
)
