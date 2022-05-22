"""``Sequence`` interface
======================

This  module declares an interface, ``SeqLike``, 
for sequence-like annotation formats. 

In terms of code in ``crowsetta``, 
a sequence-like format is any format 
that can be represented as a  
``crowsetta.Sequence`` made up of ``crowsetta.Segment``s.
The code block below shows some of the features of these data types.

.. code-block:: python

   >>> from crowsetta import Segment, Sequence
   >>> a_segment = Segment.from_keyword(
   ...     label='a',
   ...     onset_sample=16000,
   ...     offset_sample=32000,
   ...     )
   >>> another_segment = Segment.from_keyword(
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
```

"""
from .base import SeqLike
