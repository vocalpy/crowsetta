"""module for converting annotation.mat files
created by SongAnnotationGUI into Crowsetta sequences:
https://github.com/yardencsGitHub/BirdSongBout/tree/master/helpers/GUI
"""
import os
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from .annotation import Annotation
from .csv import annot2csv
from .meta import Meta
from .sequence import Sequence
from .validation import validate_ext


def _cast_to_arr(val):
    """helper function that casts single elements to 1-d numpy arrays"""
    if type(val) == int or type(val) == float:
        # this happens when there's only one syllable in the file
        # with only one corresponding label
        return np.asarray([val])  # so make it a one-element list
    elif type(val) == np.ndarray:
        # this should happen whenever there's more than one label
        return val
    else:
        # something unexpected happened
        raise TypeError(f"Type {type(val)} not recognized.")


VALID_AUDIO_FORMATS = ['wav']


def _recursive_stem(path_str):
    """helper function that 'recursively' removes file extensions
    to recover name of an audio file from the name of an array file

    i.e. bird1_122213_1534.wav.mat -> i.e. bird1_122213_1534.wav
    and i.e. bird1_122213_1534.cbin.not.mat -> i.e. bird1_122213_1534.cbin

    copied from vak library (to avoid circular dependencies upon import)
    """
    name = Path(path_str).name
    stem, ext = os.path.splitext(name)
    ext = ext.replace('.', '')
    while ext not in VALID_AUDIO_FORMATS:
        new_stem, ext = os.path.splitext(stem)
        ext = ext.replace('.', '')
        if new_stem == stem:
            raise ValueError(
                f'unable to compute stem of {path_str}'
            )
        else:
            stem = new_stem
    return stem


def yarden2annot(annot_path,
                 abspath=False,
                 basename=False,
                 round_times=True,
                 decimals=3,
                 fname_key='keys',
                 annot_key='elements',
                 onsets_key='segFileStartTimes',
                 offsets_key='segFileEndTimes',
                 labels_key='segType',
                 samp_freq_key='fs'):
    """unpack annotation.mat file into list of Sequence objects

    Parameters
    ----------
    annot_path : str
        path to .mat file of annotations, containing 'keys' and 'elements'
        where 'keys' are filenames of audio files and 'elements'
        contains additional annotation not found in .mat files
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
    fname_key : str
        name of array in .mat file that lists filenames of .mat files
        containing spectrograms. Accessed by using the array name as a
        key into a dictionary-like object, hence the name 'fname_key'.
        Default is 'keys'.
    annot_key : str
        name of array in .mat file that holds annotations for .mat files
        containing spectrograms. Default is 'elements'.
    onsets_key : str
        name of array in annotations that holds segment onset times in seconds.
        Defalt is 'segFileStartTimes'.
    offsets_key : str
        name of array in annotations that holds segment offset times in seconds.
        Defalt is 'segFileStartTimes'.
    labels_key : str
        name of array in annotations that holds label times in seconds.
        Defalt is 'segType'.
    samp_freq_key : str
        name of array in annotations that holds sample frequency of audio file.
        Defalt is 'fs'.

    Returns
    -------
    annot : list
        of Annotations

    Notes
    -----
    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful for working with multiple copies of files and for
    reproducibility. Default for both is False, in which case the filename is saved just
    as it is passed to this function.

    round_times and decimals arguments are provided to reduce differences across platforms
    due to floating point error, e.g. when loading .not.mat files and then sending them to
    a csv file, the result should be the same on Windows and Linux
    """
    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot_mat = loadmat(annot_path, squeeze_me=True)
    audio_paths = annot_mat[fname_key]
    annotations = annot_mat[annot_key]
    if len(audio_paths) != len(annotations):
        raise ValueError(f'list of filenames and list of annotations in {annot_path} do not have the same length')

    annot_list = []
    # annotation structure loads as a Python dictionary with two keys
    # one maps to a list of filenames,
    # and the other to a Numpy array where each element is the annotation
    # corresponding to the filename at the same index in the list.
    for audio_path, annotation in zip(audio_paths, annotations):
        # below, .tolist() does not actually create a list,
        # instead gets ndarray out of a zero-length ndarray of dtype=object.
        # This is just weirdness that results from loading complicated data
        # structure in .mat file.
        seq_dict = {}
        seq_dict['onsets_s'] = annotation[onsets_key].tolist()
        seq_dict['offsets_s'] = annotation[offsets_key].tolist()
        seq_dict['labels'] = annotation[labels_key].tolist()
        # cast all to numpy arrays
        seq_dict = dict((k, _cast_to_arr(seq_dict[k]))
                        for k in ['onsets_s', 'offsets_s', 'labels'])
        # after casting 'labels' to array, convert all values to string
        seq_dict['labels'] = np.asarray(
            [str(label) for label in seq_dict['labels']]
        )
        # we want to wait to add file to seq dict until *after* casting all values in dict to numpy arrays
        samp_freq = annotation[samp_freq_key].tolist()
        seq_dict['onset_inds'] = np.round(seq_dict['onsets_s'] * samp_freq).astype(int)
        seq_dict['offset_inds'] = np.round(seq_dict['offsets_s'] * samp_freq).astype(int)

        # do this *after* converting onsets_s and offsets_s to onset_inds and offset_inds
        # probably doesn't matter but why introduce more noise?
        if round_times:
            seq_dict['onset_inds'] = np.around(seq_dict['onset_inds'], decimals=decimals)
            seq_dict['offset_inds'] = np.around(seq_dict['offset_inds'], decimals=decimals)

        seq = Sequence.from_dict(seq_dict)
        annot = Annotation(seq=seq,
                           annot_path=str(annot_path),
                           audio_path=str(audio_path),
                           )
        annot_list.append(annot)

    return annot_list


def yarden2csv(annot_path, csv_filename, abspath=False, basename=False):
    """converts annotation from 'yarden'/SongAnnotationGUI-format
    .mat file(s) to `crowsetta.Annotations`, then saves
    in a comma-separated values (csv) file,
    where each row represents one annotated syllable from the file.

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
    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')
    annot = yarden2annot(annot_path)
    annot2csv(annot, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='yarden',
    ext='.mat',
    from_file=yarden2annot,
    to_csv=yarden2csv
)
