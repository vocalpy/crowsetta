"""An abstract base class for sequence-like annotation formats"""
import abc

from ..base import BaseFormat


class SeqLike(BaseFormat, abc.ABC):
    """An abstract base class defining the interface
    for any annotation format
    that can be represented as a sequence of segments,
    with each segment having an onset time,
    offset time, and a label.
    """
    def to_seq(self) -> 'Union[crowsetta.Sequence, Sequence[crowsetta.Sequence]]':
        """Converts the annotation to
        a ``crowsetta.Sequence`` instance
        or a python sequence of
        ``crowsetta.Sequence``s
        (e.g., a list or tuple).
        """
        ...
