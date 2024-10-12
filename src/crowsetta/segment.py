"""A class that represents a segment of a time series,
used to annotate animal communication."""

import attr
import numpy as np
from attr.validators import instance_of


def convert_int(val):
    """Converter that converts :class:`numpy.integer` to :class:`int`,
    returns native Python :class:`int` as is, and
    raises an error for any other type.
    """
    if hasattr(val, "dtype") and isinstance(val, np.integer):
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
    or a "syllable" in birdsong.

    Attributes
    ----------
    label: str
        The string label for the segment.
    onset_s: float, optional
        The onset time of the segment, in seconds.
    offset_s: float, optional
        The offset time of the segment, in seconds.
    onset_sample: float, optional
        The onset time of the segment, in samples
        (i.e., the index of the onset in the audio).
    offset_sample: float, optional
        The offset time of the segment, in samples
        (i.e., the index of the offset in the audio).

    Notes
    -----
    At least one of (onset_s, offset_s)
    or (onset_sample, offset_sample)
    must be specified. Both can be specified,
    but no validation is done by this class
    to make sure the time in seconds
    matches the sample number
    (since this would require the
    sampling frequency).

    Examples
    --------

    A segment with onset and offset given in seconds.

    >>> from crowsetta import Segment
    >>> Segment(label='a', onset_s=1.0, offset_s=2.0)
    Segment(label='a', onset_s=1.0, offset_s=2.0, onset_sample=None, offset_sample=None)

    A segment with onset and offset given in sample number.

    >>> Segment(label=1, onset_sample=32000, offset_sample=64000)
    Segment(label='1', onset_s=None, offset_s=None, onset_sample=32000, offset_sample=64000)

    A segment with onset and offset given in both seconds and sample number.
    Notice we give the label as an integer and it is converted to a string;
    labels are always strings.

    >>> Segment(label=1, onset_s=1.0, offset_s=2.0, onset_sample=32000, offset_sample=64000)
    Segment(label='1', onset_s=1.0, offset_s=2.0, onset_sample=32000, offset_sample=64000)
    """

    _FIELDS = ("label", "onset_s", "offset_s", "onset_sample", "offset_sample")

    label = attr.ib(converter=str)
    onset_s = attr.ib(validator=attr.validators.optional(instance_of(float)), default=None)
    offset_s = attr.ib(validator=attr.validators.optional(instance_of(float)), default=None)
    onset_sample = attr.ib(
        validator=attr.validators.optional(instance_of(int)),
        converter=attr.converters.optional(convert_int),
        default=None,
    )
    offset_sample = attr.ib(
        validator=attr.validators.optional(instance_of(int)),
        converter=attr.converters.optional(convert_int),
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
