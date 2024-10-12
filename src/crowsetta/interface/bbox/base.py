"""An abstract base class defining the interface
for any annotation format
that can be represented as a set of bounding boxes"""

import abc
from typing import Sequence, Union

from ..base import BaseFormat


class BBoxLike(BaseFormat, abc.ABC):
    """An abstract base class defining the interface
    for any annotation format
    that can be represented as a set of labeled bounding boxes.

    In terms of code in :mod:`crowsetta`,
    a bounding box-like format is any format
    that can be represented as a
    collection of :class:`crowsetta.BBox` instances.
    The code block below shows some of the features of this data type.

    .. code-block:: python

       >>> from crowsetta import BBox
       >>> a_bbox = BBox(
       ...     label='a',
       ...     onset=1.0,
       ...     offset=2.0,
       ...     low_freq=5000,
       ...     high_freq=10000,
       ...     )
       >>> another_bbox = BBox(
       ...     label='a',
       ...     onset=3.0,
       ...     offset=4.0,
       ...     low_freq=5000,
       ...     high_freq=10000,
       ...     )
       >>> list_of_bboxes = [a_bbox, another_bbox]
       >>> for bbox in list_of_bboxes: print(segment)
       BBox(onset=1.0, offset=2.0, low_freq=5000, high_freq=10000, label='a')
       BBox(onset=3.0, offset=4.0, low_freq=5000, high_freq=10000, label='a')
       >>> a_bbox.onset
       1.0
    """

    def to_bbox(self) -> "Union[crowsetta.BBox, Sequence[crowsetta.BBox]]":  # noqa : F821
        """Converts the annotation to
        a :class:`crowsetta.BBox` instance
        or a Python :class:`~typing.Sequence` of
        :class:`crowsetta.BBox` instances.
        """
        ...
