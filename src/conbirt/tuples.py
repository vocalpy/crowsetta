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
