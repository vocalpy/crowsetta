import abc

from ..base import BaseFormat


class SeqLike(BaseFormat, abc.ABC):
    """abstract base class defining the interface
    for any annotation format
    that can be represented as a sequence of segments,
    with each segment having an onset time,
    offset time, and a label.
    """
    def to_seq(self) -> 'Union[crowsetta.Sequence, Sequence[crowsetta.Sequence]]':
        """converts the annotation to
        a ``crowsetta.Sequence`` instance
        or a python sequence of
        ``crowsetta.Sequence``s
        (e.g., a list or tuple).
        """
        ...
