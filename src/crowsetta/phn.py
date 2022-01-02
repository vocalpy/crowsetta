"""module with functions that handle .phn annotation files from the TIMIT dataset
"""
import os
from pathlib import Path

import numpy as np
import soundfile

from .sequence import Sequence
from .annotation import Annotation
from .csv import annot2csv
from .meta import Meta
from .validation import validate_ext


def phn2annot(annot_path,
              abspath=False,
              basename=False,
              round_times=True,
              decimals=3):
    """parse annotation from .phn files in Timit dataset and return as Annotation

    Parameters
    ----------
    annot_path : str, Path, or list
        filename of a .phn  annotation file, or a list of paths to .phn files
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
    due to floating point error, e.g. when loading .phn files and then sending them to
    a csv file, the result should be the same on Windows and Linux
    """
    # note multiple extensions, both all-uppercase and all-lowercase `.phn` exist,
    # depending on which version of TIMIT dataset you have
    annot_path = validate_ext(annot_path, extension=('.phn', '.PHN'))

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = []
    for a_phn in annot_path:
        labels, onset_inds, offset_inds = [], [], []
        with open(a_phn) as fp:
            lines = fp.read().splitlines()
        for line in lines:
            onset, offset, label = line.split()
            onset_inds.append(int(onset))
            offset_inds.append(int(offset))
            labels.append(label)

        onset_inds = np.asarray(onset_inds)
        offset_inds = np.asarray(offset_inds)
        labels = np.asarray(labels)

        # checking for audio_pathname need to be case insensitive
        # since some versions of TIMIT dataset use .WAV instead of .wav
        audio_pathname = Path(a_phn).parent.joinpath(Path(a_phn).stem + '.wav')
        if not audio_pathname.exists():
            audio_pathname = Path(a_phn).parent.joinpath(Path(a_phn).stem + '.WAV')
            if not audio_pathname.exists():
                raise FileNotFoundError(
                    f'did not find a matching file with extension .wav or .WAV for the .phn file:\n{a_phn}'
                )

        samp_freq = soundfile.info(audio_pathname).samplerate
        onsets_s = onset_inds / samp_freq
        offsets_s = offset_inds / samp_freq

        if round_times:
            onsets_s = np.around(onsets_s, decimals=decimals)
            offsets_s = np.around(offsets_s, decimals=decimals)

        if abspath:
            audio_pathname = os.path.abspath(audio_pathname)
            a_phn = os.path.abspath(a_phn)
        elif basename:
            audio_pathname = os.path.basename(audio_pathname)
            a_phn = os.path.basename(a_phn)

        phn_seq = Sequence.from_keyword(labels=labels,
                                        onset_inds=onset_inds,
                                        offset_inds=offset_inds,
                                        onsets_s=onsets_s,
                                        offsets_s=offsets_s)
        annot.append(
            Annotation(annot_path=a_phn, audio_path=audio_pathname, seq=phn_seq)
        )

    if len(annot) == 1:
        return annot[0]
    else:
        return annot


def phn2csv(annot_path, csv_filename, abspath=False, basename=False):
    """saves annotation from .phn file(s) in a comma-separated values
    (csv) file, where each row represents one annotated segment from one
    .phn file.

    Parameters
    ----------
    annot_path : str, Path, or list
        if list, list of strings or Path objects pointing to .phn files
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
    annot_path = validate_ext(annot_path, extension=('.phn', '.PHN'))

    if abspath and basename:
        raise ValueError('abspath and basename arguments cannot both be set to True, '
                         'unclear whether absolute path should be saved or if no path '
                         'information (just base filename) should be saved.')

    annot = phn2annot(annot_path)
    annot2csv(annot, csv_filename, abspath=abspath, basename=basename)


def annot2phn(annot,
              annot_path):
    """make a .phn file from an annotation

    Parameters
    ----------
    annot : crowsetta.Annotation
        with sequence that should be converted into format of .phn files
    annot_path : Path
         path including filename where .phn file should be saved

    Returns
    -------
    None
    """
    annot_path = Path(annot_path)

    lines = []
    onset_inds, offset_inds, labels = annot.seq.onset_inds, annot.seq.offset_inds, annot.seq.labels
    for onset, offset, label in zip(onset_inds, offset_inds, labels):
        lines.append(
            f'{onset} {offset} {label}\n'
        )

    with annot_path.open('w') as fp:
        fp.writelines(lines)


meta = Meta(
    name='phn',
    ext='.phn',
    from_file=phn2annot,
    to_csv=phn2csv,
    to_format=annot2phn
)
