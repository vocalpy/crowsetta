"""An abstract base class for sequence-like annotation formats"""

import abc
from typing import Sequence, Union

from ..base import BaseFormat


class SeqLike(BaseFormat, abc.ABC):
    """An abstract base class defining the interface
    for any annotation format
    that can be represented as a sequence of segments,
    with each segment having an onset time,
    offset time, and a label.

    In terms of code in :mod:`crowsetta`,
    a sequence-like format is any format
    that can be represented as a
    :class:`crowsetta.Sequence` made up of :class:`crowsetta.Segment` instances.
    The code block below shows some of the features of these data types.

    .. code-block:: python

       >>> from crowsetta import Segment, Sequence
       >>> a_segment = Segment(
       ...     label='a',
       ...     onset_sample=16000,
       ...     offset_sample=32000,
       ...     )
       >>> another_segment = Segment(
       ...     label='b',
       ...     onset_sample=36000,
       ...     offset_sample=48000,
       ...     )
       >>> list_of_segments = [a_segment, another_segment]
       >>> seq = Sequence.from_segments(segments=list_of_segments)
       >>> print(seq)
       <Sequence with 2 segments>
       >>> for segment in seq.segments: print(segment)
       Segment(label='a', onset_s=None, offset_s=None, onset_ind=16000, offset_ind=32000)
       Segment(label='b', onset_s=None, offset_s=None, onset_ind=36000, offset_ind=48000)
       >>> seq.onset_inds
       array([16000, 36000])
    """

    def to_seq(self) -> "Union[crowsetta.Sequence, Sequence[crowsetta.Sequence]]":  # noqa : F821
        """Converts the annotation to
        a ``crowsetta.Sequence`` instance
        or a python sequence of
        ``crowsetta.Sequence``s
        (e.g., a list or tuple).
        """
        ...
