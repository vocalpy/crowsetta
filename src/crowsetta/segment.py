"""A class that represents a segment of a time series,
used to annotate animal communication."""
import attr
import numpy as np
from attr.validators import instance_of


def int64_to_int(val):
    """Converter that converts ``numpy.int64`` to ``int``,
    returns ``int`` as is, and errors for other values.
    """
    if hasattr(val, "dtype"):
        if val.dtype == np.int64:
            return int(val)
    elif isinstance(val, int):
        return val
    else:
        raise TypeError(f"Invalid type {type(val)} for onset or offset sample: {val}. Must be an integer.")


@attr.s(frozen=True)
class Segment(object):
    """A class that represents a segment of a time series,
    used to annotate animal communication.

    Typically, a single unit such as a syllable in human speech
    or a "syllable" in birdsong."""

    _FIELDS = ("label", "onset_s", "offset_s", "onset_sample", "offset_sample")

    label = attr.ib(converter=str)
    onset_s = attr.ib(validator=attr.validators.optional(instance_of(float)), default=None)
    offset_s = attr.ib(validator=attr.validators.optional(instance_of(float)), default=None)
    onset_sample = attr.ib(
        validator=attr.validators.optional(instance_of(int)),
        converter=attr.converters.optional(int64_to_int),
        default=None,
    )
    offset_sample = attr.ib(
        validator=attr.validators.optional(instance_of(int)),
        converter=attr.converters.optional(int64_to_int),
        default=None,
    )
    asdict = attr.asdict

    def __attrs_post_init__(self):
        if (self.onset_sample is None and self.offset_sample is None) and (
            self.onset_s is None and self.offset_s is None
        ):
            raise ValueError("must provide either onset_sample and offset_sample, or " "onsets_s and offsets_s")

        if self.onset_sample and self.offset_sample is None:
            raise ValueError(f"onset_sample specified as {self.onset_sample} but offset_sample is None")
        if self.onset_sample is None and self.offset_sample:
            raise ValueError(f"offset_sample specified as {self.offset_sample} but onset_sample is None")
        if self.onset_s and self.offset_s is None:
            raise ValueError(f"onset_s specified as {self.onset_s} but offset_s is None")
        if self.onset_s is None and self.offset_s:
            raise ValueError(f"offset_s specified as {self.offset_sample} but onset_s is None")
