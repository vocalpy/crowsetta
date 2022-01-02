"""module with functions that handle the following dataset:
data: https://figshare.com/articles/BirdsongRecognition/3470165

as used in this paper:
[1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""
import os
from pathlib import Path
import numpy as np

import birdsongrec
import soundfile

from .annotation import Annotation
from .sequence import Sequence
from . import csv
from .meta import Meta


def birdsongrec2annot(annot_path='Annotation.xml', concat_seqs_into_songs=True,
                      wavpath=None):
    """converts Annotation.xml from [1]_ into an annotation list

    Parameters
    ----------
    annot_path : str, pathlib.Path
        Path to .xml file from BirdsongRecognition dataset that contains annotation.
        Default is 'Annotation.xml'.
    concat_seqs_into_songs : bool
        if True, concatenate sequences from xml_file, so that
        one sequence = one song / .wav file. Default is True.
    wavpath : str, pathlib.Path
        Path in which .wav files listed in Annotation.xml file are found.
        Default is None, in which case function assumes that the files are
        in a directory `Wave` that is located in the parent directory of
        the Annotation.xml file, which matches the structure of the dataset from [1]_.

            Bird4/
                Annotation.xml
                Wave/
                    0.wav
                    1.wav
                    ...

    Returns
    -------
    seq_list : list
        of Sequence objects

    [1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
    Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
    doi:10.1371/journal.pone.0159188
    """
    annot_path = Path(annot_path).expanduser().resolve()
    if not annot_path.suffix == '.xml':
        raise ValueError(
            "Annotation file format should be xml, but value for 'annot_path' does not end in '.xml'.\n"
            f"Value was: {annot_path}"
        )
    if not annot_path.exists():
        raise FileNotFoundError(
            f"annot_path not found: {annot_path}"
        )

    if wavpath is None:
        wavpath = annot_path.parent.joinpath('Wave')
    else:
        wavpath = Path(wavpath)

    if not wavpath.exists():
        raise NotADirectoryError(
            "Value specified for 'wavpath' not recognized as an existing directory."
            f"\nValue for 'wavpath' was: {wavpath}"
        )

    # `birdsong-recongition-dataset` also has a 'Sequence' class
    # but it is slightly different from the `generic.Sequence` used by `crowsetta`
    seq_list_xml = birdsongrec.parse_xml(annot_path,
                                         concat_seqs_into_songs=concat_seqs_into_songs)

    annot_list = []
    for seq_xml in seq_list_xml:
        onset_inds = np.asarray([syl.position for syl in seq_xml.syls])
        offset_inds = np.asarray([syl.position + syl.length for syl in seq_xml.syls])
        labels = [syl.label for syl in seq_xml.syls]

        wav_filename = os.path.join(wavpath, seq_xml.wav_file)
        wav_filename = os.path.abspath(wav_filename)
        if not os.path.isfile(wav_filename):
            raise FileNotFoundError(
                f'.wav file {wav_filename} specified in '
                f'annotation file {annot_path} is not found'
            )
        samp_freq = soundfile.info(wav_filename).samplerate
        onsets_s = np.round(onset_inds / samp_freq, decimals=3)
        offsets_s = np.round(offset_inds / samp_freq, decimals=3)

        seq = Sequence.from_keyword(onset_inds=onset_inds,
                                    offset_inds=offset_inds,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s,
                                    labels=labels
                                    )
        annot = Annotation(seq=seq, annot_path=annot_path, audio_path=wav_filename)
        annot_list.append(annot)
    return annot_list


def birdsongrec2csv(annot_path, concat_seqs_into_songs=True, wavpath='./Wave',
                    csv_filename=None, abspath=False, basename=False):
    """takes Annotation.xml file from BirdsongRecognition dataset
    and saves the annotation from all files in one comma-separated
    values (csv) file, where each row represents one syllable from
    one of the .wav files.

    Parameters
    ----------
    annot_path : str
        filename of 'Annotation.xml' file
    concat_seqs_into_songs : bool
        if True, concatenate 'sequences' from annotation file
        by song (i.e., .wav file that sequences are found in).
        Default is True.
    wavpath : str
        Path in which .wav files listed in Annotation.xml file are found.
        By default this is './Wave' to match the structure of the original
        repository.
    csv_filename : str
        Optional, name of .csv file to save. Defaults to None,
        in which case name is xml_file, but with
        extension changed to .csv.

    Other Parameters
    ----------------
    abspath : bool
        if True, converts filename for each audio file into absolute path.
        Default is False.
    basename : bool
        if True, discard any information about path and just use file name.
        Default is False.

    Returns
    -------
    None

    Notes
    -----
    see annot2scv function for explanation of when you would want to use
    the abspath and basename parameters
    """
    annot = birdsongrec2annot(annot_path, concat_seqs_into_songs=concat_seqs_into_songs,
                              wavpath=wavpath)
    if csv_filename is None:
        csv_filename = os.path.abspath(annot_path)
        csv_filename = csv_filename.replace('xml', 'csv')
    csv.annot2csv(annot, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='birdsong-recognition-dataset',
    ext='xml',
    from_file=birdsongrec2annot,
    to_csv=birdsongrec2csv,
)
