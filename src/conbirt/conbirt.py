import os
import csv

import numpy as np


# fields that must be present for each syllable that is annotated.
# these field names are used below by annot_list_to_csv and csv_to_annot_list
# but defined at top-level of the module, since these fields determine
# what annotations the library can and cannot interpret.
# The idea is to use the bare minimum of fields required.
SYL_ANNOT_COLUMN_NAMES = ['filename',
                          'onset_Hz',
                          'offset_Hz',
                          'onset_s',
                          'offset_s',
                          'label']
set_SYL_ANNOT_COLUMN_NAMES = set(SYL_ANNOT_COLUMN_NAMES)

# below maps each column in csv to a key in an annot_dict
# used when appending to lists that correspond to each key
SYL_ANNOT_TO_SONG_ANNOT_MAPPING = {'onset_Hz':'onsets_Hz',
                                   'offset_Hz': 'offsets_Hz',
                                   'onset_s': 'onsets_s',
                                   'offset_s': 'offsets_s',
                                   'label': 'labels'}

# used when mapping inputs **from** csv **to** annotation
SONG_ANNOT_TYPE_MAPPING = {'onsets_Hz': int,
                           'offsets_Hz': int,
                           'onsets_s': float,
                           'offsets_s': float,
                           'labels': str}


def func2seq(func, files):
    """converts files into Sequences using a user-specified function

    Parameters
    ----------
    func : function
    files : iterable or str

    Returns
    -------
    seq : Sequence
    """
    seq_list = []
    for file in files:
        seq_list.append(func(file))
    if len(seq_list) == 1:
        seq_list = seq_list[0]
    return seq_list



class Conbirter:
    """class that handles conversion from different annotation formats into
    lists of Sequence objects and/or csv files"""
    def __init__(self):
        pass

    def to_seq(self, file):
        for file in files:
            seq = func(file)

    def to_seqlist(self, files, format=None):
        for file in files:
            seq = func(file)


    def to_csv(self, files):