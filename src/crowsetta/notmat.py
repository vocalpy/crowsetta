"""module with functions that handle .not.mat annotation files
produced by evsonganaly GUI
"""
import os
from pathlib import Path

import numpy as np
import scipy.io
import evfuncs

from .classes import Sequence
from .csv import seq2csv


def _parse_notmat(notmat):
    """helper function that parses/validates value for notmat argument;
    puts a single string or Path into a list to iterate over it (cheap hack
    that lets functions accept multiple types), and checks list to make sure
    all types are consistent
    """
    if type(notmat) == str or type(notmat) == Path:
        # put in a list to iterate over
        notmat = [notmat]

    for a_notmat in notmat:
        if type(a_notmat) == str:
            if not a_notmat.endswith('.not.mat'):
                raise ValueError("all filenames in .not.mat must end with '.not.mat' "
                                 f"but {a_notmat} does not")
        elif type(a_notmat) == Path:
            if not a_notmat.suffixes == ['.not', '.mat']:
                raise ValueError("all filenames in .not.mat must end with '.not.mat' "
                                 f"but {a_notmat} does not")

    return notmat


def notmat2seq(notmat,
               abspath=False,
               basename=False,
               round_times=True,
               decimals=3):
    """open .not.mat file and return as Sequence
    (data structure that used internally to represent
    annotation for one audio file)

    Parameters
    ----------
    notmat : str, Path, or list
        filename of a .not.mat annotation file,
        created by the evsonganaly GUI for MATLAB
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
    seq : Sequence
        with fields 'file', 'labels', 'onsets_Hz', 'offsets_Hz', 'onsets_s', 'offsets_s'

    The abspath and basename parameters specify how file names for audio files are saved.
    These options are useful for working with multiple copies of files and for
    reproducibility. Default for both is False, in which case the filename is saved just
    as it is passed to this function.

    round_times and decimals arguments are provided to reduce differences across platforms
    due to floating point error, e.g. when loading .not.mat files and then sending them to
    a csv file, the result should be the same on Windows and Linux
    """
    notmat = _parse_notmat(notmat)

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    seq = []
    for a_notmat in notmat:
        notmat_dict = evfuncs.load_notmat(a_notmat)
        # in .not.mat files saved by evsonganaly,
        # onsets and offsets are in units of ms, have to convert to s
        onsets_s = notmat_dict['onsets'] / 1000
        offsets_s = notmat_dict['offsets'] / 1000
    
        # convert to Hz using sampling frequency
        audio_filename = a_notmat.replace('.not.mat','')
        if audio_filename.endswith('.cbin'):
            rec_filename = audio_filename.replace('.cbin','.rec')
        elif audio_filename.endswith('.wav'):
            rec_filename = audio_filename.replace('.wav', '.rec')
        else:
            raise ValueError("Can't find .rec file for {}."
                             .format(a_notmat))
        rec_dict = evfuncs.readrecf(rec_filename)
        sample_freq = rec_dict['sample_freq']
        # subtract one because of Python's zero indexing (first sample is sample zero)
        onsets_Hz = np.round(onsets_s * sample_freq).astype(int) - 1
        offsets_Hz = np.round(offsets_s * sample_freq).astype(int)
    
        # do this *after* converting onsets_s and offsets_s to onsets_Hz and offsets_Hz
        # probably doesn't matter but why introduce more noise?
        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)
    
        if abspath:
            audio_filename = os.path.abspath(audio_filename)
        elif basename:
            audio_filename = os.path.basename(audio_filename)

        seq.append(Sequence(file=audio_filename,
                            labels=np.asarray(list(notmat_dict['labels'])),
                            onsets_s=onsets_s,
                            offsets_s=offsets_s,
                            onsets_Hz=onsets_Hz,
                            offsets_Hz=offsets_Hz)
                   )

    if len(seq) == 1:
        return seq[0]
    else:
        return seq 


def notmat2csv(notmat, csv_filename, abspath=False, basename=False):
    """saves annotation from .not.mat file(s) in a comma-separated values
    (csv) file, where each row represents one syllable from one
    .not.mat file.

    Parameters
    ----------
    notmat : str, Path, or list
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
    notmat = _parse_notmat(notmat)

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    seq = notmat2seq(notmat)
    seq2csv(seq, csv_filename, abspath=abspath, basename=basename)


def make_notmat(filename,
                labels,
                onsets_Hz,
                offsets_Hz,
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
    onsets_Hz : ndarray
        onsets of syllables in sample number.
    offsets_Hz : ndarray
        offsets of syllables in sample number.
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
    onsets_s = onsets_Hz / samp_freq
    offsets_s = offsets_Hz / samp_freq
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
