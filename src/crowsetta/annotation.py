from pathlib import Path

import attr
from attr import validators, converters
from attr.validators import instance_of

from .sequence import Sequence


@attr.s
class Annotation:
    """a class to represent annotations for a single file"""
    annot_path = attr.ib(converter=Path)
    audio_path = attr.ib(converter=converters.optional(Path), default=None)
    seq = attr.ib(validator=validators.optional(instance_of(Sequence)), default=None)
