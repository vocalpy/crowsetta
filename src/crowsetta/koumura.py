"""module with functions that handle the following dataset:
data: https://figshare.com/articles/BirdsongRecognition/3470165

as used in this paper:
[1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""
import os

import numpy as np
import wave

import koumura

from .sequence import Sequence
from . import csv
from .meta import Meta


def koumura2seq(file='Annotation.xml', concat_seqs_into_songs=True,
                wavpath='./Wave'):
    """converts Annotation.xml from [1]_ into an annotation list

    Parameters
    ----------
    file : str or pathlib.Path
        Path to Annotation.xml
    concat_seqs_into_songs : bool
        if True, concatenate sequences from xml_file, so that
        one sequence = one song / .wav file. Default is True.
    wavpath : str
        Path in which .wav files listed in Annotation.xml file are found.
        By default this is './Wave' to match the structure of the original
        repository.

    Returns
    -------
    seq_list : list
        of Sequence objects

    [1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
    Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
    doi:10.1371/journal.pone.0159188
    """
    wavpath = os.path.normpath(wavpath)
    if not os.path.isdir(wavpath):
        raise NotADirectoryError('Path specified for wavpath, {}, not recognized as an '
                                 'existing directory'.format(wavpath))

    if not file.endswith('.xml'):
        raise ValueError('Name of annotation file should end with .xml, '
                         'but name passed was {}'.format(xml_file))

    # confusingly, koumura also has an object named 'Sequence'
    # (which is where I borrowed the idea from)
    # but it has a totally different structure
    seq_list_xml = koumura.parse_xml(file, concat_seqs_into_songs=concat_seqs_into_songs)

    seq_list_out = []
    for seq_xml in seq_list_xml:
        onsets_Hz = np.asarray([syl.position for syl in seq_xml.syls])
        offsets_Hz = np.asarray([syl.position + syl.length for syl in seq_xml.syls])
        labels = [syl.label for syl in seq_xml.syls]

        wav_filename = os.path.join(wavpath, seq_xml.wav_file)
        wav_filename = os.path.abspath(wav_filename)
        if not os.path.isfile(wav_filename):
            raise FileNotFoundError('.wav file {} specified in annotation file {} is not found'
                                    .format(wav_filename, annotation_file))
        # found with %%timeit that Python wave module takes about 1/2 the time of
        # scipy.io.wavfile for just reading sampling frequency from each file
        with wave.open(wav_filename, 'rb') as wav_file:
            samp_freq = wav_file.getframerate()
        onsets_s = np.round(onsets_Hz / samp_freq, decimals=3)
        offsets_s = np.round(offsets_Hz / samp_freq, decimals=3)

        seq_obj = Sequence.from_keyword(
            file=seq_xml.wav_file,
            onsets_Hz=onsets_Hz,
            offsets_Hz=offsets_Hz,
            onsets_s=onsets_s,
            offsets_s=offsets_s,
            labels=labels
        )
        seq_list_out.append(seq_obj)
    return seq_list_out


def koumura2csv(file, concat_seqs_into_songs=True, wavpath='./Wave',
                csv_filename=None, abspath=False, basename=False):
    """takes Annotation.xml file from Koumura dataset into and saves the
    annotation from all files in one comma-separated values (csv)
    file, where each row represents one syllable from one of the
    .wav files.

    Parameters
    ----------
    xml_file : str
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
    see seq2scv function for explanation of when you would want to use
    the abspath and basename parameters
    """
    seq_list = koumura2seq(file, concat_seqs_into_songs=concat_seqs_into_songs,
                           wavpath=wavpath)
    if csv_filename is None:
        csv_filename = os.path.abspath(file)
        csv_filename = csv_filename.replace('xml', 'csv')
    csv.seq2csv(seq_list, csv_filename, abspath=abspath, basename=basename)


meta = Meta(
    name='koumura',
    ext='xml',
    to_seq=koumura2seq,
    to_csv=koumura2csv,
)
