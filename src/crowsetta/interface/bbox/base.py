"""An abstract base class defining the interface
for any annotation format
that can be represented as a set of bounding boxes"""
import abc

from ..base import BaseFormat


class BBoxLike(BaseFormat, abc.ABC):
    """An abstract base class defining the interface
    for any annotation format
    that can be represented as a set of bounding boxes,
    where each bounding box has corners
    ((x_min, y_max), (x_min, y_min), (x_max, y_max), (x_max, y_min))
    and a label.
    """
    def to_bbox(self) -> 'Union[crowsetta.BBox, Sequence[crowsetta.BBox]]':
        """Converts the annotation to
        a ``crowsetta.BBox`` instance
        or a python set of
        ``crowsetta.BBox`` instances.
        """
        ...
