"""defines Sequence object used for conversion"""
from collections import namedtuple

import numpy as np
import attr


class Sequence:
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
    }, init=False)(Sequence)

# Sequence = namedtuple('Sequence', ['onsets_Hz',
#                                    'offsets_Hz',
#                                    'onsets_s',
#                                    'offsets_s',
#                                    'labels',
#                                    'file',
#                                    ]
#                       )

Segment = namedtuple('Segment', ['onset_Hz',
                                 'offset_Hz',
                                 'onset_s',
                                 'offset_s',
                                 'label',
                                 'file',
                                 ]
                     )
