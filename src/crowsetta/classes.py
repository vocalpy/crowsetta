"""defines Sequence object used for conversion"""
from collections import namedtuple

import numpy as np
import attr


# Segment = namedtuple('Segment', ['onset_Hz',
#                                  'offset_Hz',
#                                  'onset_s',
#                                  'offset_s',
#                                  'label',
#                                  'file',
#                                  ]
#                      )


class SegmentClass(object):
    """object that represents a segment of a time series,
     usually a syllable in a bout of birdsong"""
    def __init__(self, label, file, onset_s=None, offset_s=None,
                 onset_Hz=None, offset_Hz=None):
        if ((onset_Hz is None and offset_Hz is None) and
                (onset_s is None and offset_s is None)):
            raise ValueError('must provide either onset_Hz and offset_Hz, or '
                             'onsets_s and offsets_s')

        if onset_Hz and offset_Hz is None:
            raise ValueError(f'onset_Hz specified as {onset_Hz} but offset_Hz is None')
        if onset_Hz is None and offset_Hz:
            raise ValueError(f'offset_Hz specified as {offset_Hz} but onset_Hz is None')
        if onset_s and offset_s is None:
            raise ValueError(f'onset_s specified as {onset_s} but offset_s is None')
        if onset_s is None and offset_s:
            raise ValueError(f'offset_s specified as {offset_Hz} but onset_s is None')

        self.label = label
        self.file = file
        self.onset_s = onset_s
        self.offset_s = offset_s
        self.onset_Hz = onset_Hz
        self.offset_Hz = offset_Hz


Segment = attr.s(
    these={
        'file': attr.ib(type=str),
        'onset_Hz': attr.ib(type=int),
        'offset_Hz': attr.ib(type=int),
        'onset_s': attr.ib(type=float),
        'offset_s': attr.ib(type=float),
        'label': attr.ib(type=str),
    }, init=False)(SegmentClass)


class SequenceClass:
    """object that represents a sequence of segments, such as a bout of birdsong made
    up of syllables, with the following fields:
        file : str
            name of audio file with which annotation is associated.
            See parameter abspath and basename below that allow for specifying how
            filename is saved.
        onsets_Hz : numpy.ndarray
            of type int, onset of each annotated segment in samples/second
        offsets_Hz : numpy.ndarray
            of type int, offset of each annotated segment in samples/second
        onsets_s : numpy.ndarray
            of type float, onset of each annotated segment in seconds
        offsets_s : numpy.ndarray
            of type float, offset of each annotated segment in seconds
        labels : numpy.ndarray
            of type str, label for each annotated segment
    """
    def __init__(self, file, labels,
                 onsets_Hz=None, offsets_Hz=None,
                 onsets_s=None, offsets_s=None):
        if ((onsets_Hz is None and offsets_Hz is None) and
                (onsets_s is None and offsets_s is None)):
            raise ValueError('must provide either onsets_Hz and offsets_Hz, or '
                             'onsets_s and offsets_s')
        if (onsets_Hz is not None and offsets_Hz is not None):
            if onsets_Hz.dtype != int or offsets_Hz.dtype != int:
                raise TypeError('dtype of onsets_Hz and offsets_Hz must be some kind of int')
        if (onsets_s is not None and offsets_s is not None):
            if onsets_s.dtype != float or offsets_s.dtype != float:
                raise TypeError('dtype of onsets_s and offsets_s must be some kind of float')

        self.file = file
        self.onsets_Hz = onsets_Hz
        self.offsets_Hz = offsets_Hz
        self.onsets_s = onsets_s
        self.offsets_s = offsets_s
        self.labels = labels


Sequence = attr.s(
    these={
        'file': attr.ib(type=str),
        'onsets_Hz': attr.ib(type=np.ndarray),
        'offsets_Hz': attr.ib(type=np.ndarray),
        'onsets_s': attr.ib(type=np.ndarray),
        'offsets_s': attr.ib(type=np.ndarray),
        'labels': attr.ib(type=np.ndarray),
    }, init=False)(SequenceClass)
