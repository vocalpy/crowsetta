"""module with functions that handle a simple .csv annotation format"""
import os

import numpy as np
import pandas as pd
import scipy.io

from .sequence import Sequence
from .annotation import Annotation
from .csv import annot2csv
from .meta import Meta
from .validation import validate_ext


def simple2annot(annot_path,
                 abspath=False,
                 basename=False,
                 round_times=True,
                 decimals=3):
    """parse annotation from simple .csv files,
    and load into ``crowsetta.Annotation``s

    Parameters
    ----------
    annot_path : str, Path, or list
        filename of a .csv annotation file,
        or a list of paths to .csv files
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

    Returns
    -------
    annot : Annotation, list
        if a single file is provided, a single Annotation is returned. If a list is
        provided, a list of Annotations is returned. Annotation will have a `sequence`
        attribute with the fields 'file', 'labels', 'onsets_s', 'offsets_s'

    Notes
    -----
    .csv files parsed by this function should have the following format:
    3 columns: 'onsets_s', 'offsets_s', and 'labels`.
    There should be a header with those column names.
    The annotation file should have the same name as the audio file that
    it annotates, with the extension .csv added.
    E.g., if the audio file is named 'fly1-2020-12-03.wav' then the .csv file
    should be named 'fly1-2020-12-03.wav.csv'.

    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful for working with multiple copies of files and for
    reproducibility. Default for both is False, in which case the filename is saved just
    as it is passed to this function.

    round_times and decimals arguments are provided to reduce differences across platforms
    due to floating point error, e.g. when loading .not.mat files and then sending them to
    a csv file, the result should be the same on Windows and Linux
    """
    annot_path = validate_ext(annot_path, extension='.csv')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = []
    for a_csv in annot_path:
        df = pd.read_csv(a_csv)
        onsets_s = df['onset_s'].values
        offsets_s = df['offset_s'].values

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        audio_pathname = a_csv.replace('.csv', '')
        if abspath:
            audio_pathname = os.path.abspath(audio_pathname)
            a_csv = os.path.abspath(a_csv)
        elif basename:
            audio_pathname = os.path.basename(audio_pathname)
            a_csv = os.path.basename(a_csv)

        csv_seq = Sequence.from_keyword(labels=df['label'].values,
                                        onsets_s=onsets_s,
                                        offsets_s=offsets_s)
        annot.append(
            Annotation(annot_path=a_csv, audio_path=audio_pathname, seq=csv_seq)
        )

    if len(annot) == 1:
        return annot[0]
    else:
        return annot


def simple2csv(annot_path, csv_filename, abspath=False, basename=False):
    """converts annotation from a simple .csv file format into
    ``crowsetta.Annotation``s, and then saves those ``Annotation``s
    to a .csv file

    Parameters
    ----------
    annot_path : str, Path, or list
        if list, list of strings or Path objects pointing to .not.mat files
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
    annot_path = validate_ext(annot_path, extension='.csv')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = simple2annot(annot_path)
    annot2csv(annot, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='simple-csv',
    ext='csv',
    from_file=simple2annot,
    to_csv=simple2csv,
)
