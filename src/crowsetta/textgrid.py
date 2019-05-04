"""module for loading Praat TextGrid files into Sequences

uses the Python library textgrid
https://github.com/kylebgorman/textgrid
a version is distributed with this code (../textgrid) under MIT license
https://github.com/kylebgorman/textgrid/blob/master/LICENSE
"""
import os

import numpy as np
from textgrid import TextGrid, IntervalTier

from .sequence import Sequence
from .meta import Meta
from .csv import seq2csv
from .validation import _parse_file


def textgrid2seq(file,
                 abspath=False,
                 basename=False,
                 round_times=True,
                 decimals=3,
                 intervaltier_ind=0,
                 audio_ext='wav',
                 ):
    """convert Praat Textgrid file into a Sequence

    Parameters
    ----------
    file : str, Path
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
    seq : crowsetta.Sequence or list of Sequence
        each Interval in the first IntervalTier in a TextGrid file
        will become one segment in a sequence.
    """
    file = _parse_file(file, extension='.TextGrid')
    seq = []
    for a_textgrid in file:
        tg = TextGrid.fromFile(a_textgrid)

        intv_tier = tg[intervaltier_ind]
        if type(intv_tier) != IntervalTier:
            raise ValueError(f'Index specified for IntervalTier was {intervaltier_ind}, '
                             f'but type at that index was {type(intv_tier)}, not an IntervalTier')

        audio_filename = a_textgrid.replace('TextGrid', audio_ext)
        if abspath:
            audio_filename = os.path.abspath(audio_filename)
        elif basename:
            audio_filename = os.path.basename(audio_filename)

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

        textgrid_seq = Sequence.from_keyword(file=audio_filename,
                                             labels=labels,
                                             onsets_s=onsets_s,
                                             offsets_s=offsets_s)
        seq.append(textgrid_seq)

    if len(seq) == 1:
        return seq[0]
    else:
        return seq


def textgrid2csv(file, csv_filename, abspath=False, basename=False):
    """saves annotation from TextGrid file(s) in a comma-separated values
    (csv) file, where each row represents one syllable from one
    .not.mat file.

    Parameters
    ----------
    file : str, Path, or list
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
    file = _parse_file(file, extension='.TextGrid')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    seq = textgrid2seq(file)
    seq2csv(seq, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='textgrid',
    ext='TextGrid',
    to_seq=textgrid2seq,
    to_csv=textgrid2csv,
)
