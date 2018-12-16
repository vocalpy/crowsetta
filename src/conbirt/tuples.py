"""
        each Sequence object has the following fields:
            file : str
                name of audio file with which annotation is associated.
                See parameter abspath and basename below that allow for specifying how
                filename is saved.
            onsets_Hz : numpy.ndarray
                of type int, onset of each annotated syllable in samples/second
            offsets_Hz : numpy.ndarray
                of type int, offset of each annotated syllable in samples/second
            onsets_s : numpy.ndarray
                of type float, onset of each annotated syllable in seconds
            offsets_s : numpy.ndarray
                of type float, offset of each annotated syllable in seconds
            labels : numpy.ndarray
                of type str, label for each annotated syllable
"""
from collections import namedtuple

Sequence = namedtuple('Sequence', ['onsets_Hz',
                                   'offsets_Hz',
                                   'onsets_s',
                                   'offsets_s',
                                   'labels',
                                   'file',
                                   ]
                      )

Segment = namedtuple('Segment', ['onset_Hz',
                                 'offset_Hz',
                                 'onset_s',
                                 'offset_s',
                                 'label',
                                 'file',
                                 ]
                     )
