import attr
from attr.validators import optional, instance_of

from .sequence import Sequence


@attr.s
class Annotation:
    """a class to represent annotations for a single file"""
    file = attr.ib(validator=instance_of(str))
    seq = attr.ib(validator=optional(instance_of(Sequence)), default=None)
