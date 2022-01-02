"""module with functions that handle .not.mat annotation files
produced by evsonganaly GUI
"""
import os

import numpy as np
import scipy.io
import evfuncs

from .sequence import Sequence
from .annotation import Annotation
from .csv import annot2csv
from .meta import Meta
from .validation import validate_ext


def notmat2annot(annot_path,
                 abspath=False,
                 basename=False,
                 round_times=True,
                 decimals=3):
    """parse annotation from .not.mat and return as Annotation

    Parameters
    ----------
    annot_path : str, Path, or list
        filename of a .not.mat annotation file, created by the evsonganaly GUI for MATLAB,
        or a list of paths to .not.mat files
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

    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful for working with multiple copies of files and for
    reproducibility. Default for both is False, in which case the filename is saved just
    as it is passed to this function.

    round_times and decimals arguments are provided to reduce differences across platforms
    due to floating point error, e.g. when loading .not.mat files and then sending them to
    a csv file, the result should be the same on Windows and Linux
    """
    annot_path = validate_ext(annot_path, extension='.not.mat')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = []
    for a_notmat in annot_path:
        notmat_dict = evfuncs.load_notmat(a_notmat)
        # in .not.mat files saved by evsonganaly,
        # onsets and offsets are in units of ms, have to convert to s
        onsets_s = notmat_dict['onsets'] / 1000
        offsets_s = notmat_dict['offsets'] / 1000

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        audio_pathname = a_notmat.replace('.not.mat', '')
        if abspath:
            audio_pathname = os.path.abspath(audio_pathname)
            a_notmat = os.path.abspath(a_notmat)
        elif basename:
            audio_pathname = os.path.basename(audio_pathname)
            a_notmat = os.path.basename(a_notmat)

        notmat_seq = Sequence.from_keyword(labels=np.asarray(list(notmat_dict['labels'])),
                                           onsets_s=onsets_s,
                                           offsets_s=offsets_s)
        annot.append(
            Annotation(annot_path=a_notmat, audio_path=audio_pathname, seq=notmat_seq)
        )

    if len(annot) == 1:
        return annot[0]
    else:
        return annot


def notmat2csv(annot_path, csv_filename, abspath=False, basename=False):
    """saves annotation from .not.mat file(s) in a comma-separated values
    (csv) file, where each row represents one syllable from one
    .not.mat file.

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
    annot_path = validate_ext(annot_path, extension='.not.mat')

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = notmat2annot(annot_path)
    annot2csv(annot, csv_filename, abspath=abspath, basename=basename)


def make_notmat(filename,
                labels,
                onsets_s,
                offsets_s,
                samp_freq,
                threshold,
                min_syl_dur,
                min_silent_dur,
                alternate_path=None,
                other_vars=None):
    """make a .not.mat file
    that can be read by evsonganaly (MATLAB GUI for labeling song)

    Parameters
    ----------
    filename : str
        name of audio file associated with .not.mat,
        will be used as base of name for .not.mat file
        e.g., if filename is
        'bl26lb16\041912\bl26lb16_190412_0721.20144.cbin'
        then the .not.mat file will be
        'bl26lb16\041912\bl26lb16_190412_0721.20144.cbin.not.mat'
    labels : ndarray
        of type str.
        array of labels given to segments, i.e. syllables, found in filename
    onsets_s : ndarray
        onsets of syllables in seconds.
    offsets_s : ndarray
        offsets of syllables in seconds.
    samp_freq : int
        sampling frequency of audio file
    threshold : int
        value above which amplitude is considered part of a segment. default is 5000.
    min_syl_dur : float
        minimum duration of a segment. default is 0.02, i.e. 20 ms.
    min_silent_dur : float
        minimum duration of silent gap between segment. default is 0.002, i.e. 2 ms.
    alternate_path : str
        Alternate path to which .not.mat files should be saved
        if .not.mat files with same name already exist in directory
        containing audio files.
        Default is None.
        Labelpredict assigns the output_dir from the
        predict.config.yml file as an alternate.
    other_vars : dict
        mapping from variable names to other variables that should be saved
        in the .not.mat file, e.g. if you need to add a variable named 'pitches'
        that is an numpy array of float values

    Returns
    -------
    None
    """
    if other_vars is not None:
        if type(other_vars) != dict:
            raise TypeError(f'other_vars must be a dict, not a {type(other_vars)}')
        if not all(type(key) == str for key in other_vars.keys()):
            raise TypeError('all keys for other_vars dict must be of type str')

    # chr() to convert back to character from uint32
    if labels.dtype == 'int32':
        labels = [chr(val) for val in labels]
    elif labels.dtype == '<U1':
        labels = labels.tolist()
    # convert into one long string, what evsonganaly expects
    labels = ''.join(labels)
    # notmat files have onsets/offsets in units of ms
    # need to convert back from s
    onsets = (onsets_s * 1e3).astype(float)
    offsets = (offsets_s * 1e3).astype(float)

    # same goes for min_int and min_dur
    # also wrap everything in float so Matlab loads it as double
    # because evsonganaly expects doubles
    notmat_dict = {'fname': filename,
                   'Fs': float(samp_freq),
                   'min_dur': float(min_syl_dur * 1e3),
                   'min_int': float(min_silent_dur * 1e3),
                   'offsets': offsets,
                   'onsets': onsets,
                   'sm_win': float(2),  # evsonganaly.m doesn't actually let user change this value
                   'threshold': float(threshold)
                   }
    notmat_dict['labels'] = labels

    if other_vars:
        for var_name, var in other_vars.items():
            notmat_dict[var_name] = var

    notmat_name = filename + '.not.mat'
    if os.path.exists(notmat_name):
        if alternate_path:
            alternate_notmat_name = os.path.join(alternate_path,
                                                 os.path.basename(filename)
                                                 + '.not.mat')
            if os.path.exists(alternate_notmat_name):
                raise FileExistsError('Tried to save {} in alternate path {},'
                                      'but file already exists'.format(alternate_notmat_name,
                                                                       alternate_path))
            else:
                scipy.io.savemat(alternate_notmat_name, notmat_dict)
        else:
            raise FileExistsError('{} already exists but no alternate path provided'
                                  .format(notmat_name))
    else:
        scipy.io.savemat(notmat_name, notmat_dict)


meta = Meta(
    name='notmat',
    ext='not.mat',
    from_file=notmat2annot,
    to_csv=notmat2csv,
    to_format=make_notmat,
)
