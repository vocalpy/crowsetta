import os
import csv

import numpy as np


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
        pass
