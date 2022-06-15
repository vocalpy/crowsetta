"""A class that represents a segment of a time series, 
used to annotate animal communication."""
import warnings

import attr


def float_or_None(val):
    """converter that casts val to float, or returns None if val is string 'None'"""
    if val == 'None':
        return None
    else:
        return float(val)


def int_or_None(val):
    """converter that casts val to int, or returns None if val is string 'None'"""
    if val == 'None':
        return None
    else:
        return int(val)


@attr.s(frozen=True)
class Segment(object):
    """A class that represents a segment of a time series,
    used to annotate animal communication.

    Typically, a single unit such as a syllable in human speech
    or a "syllable" in birdsong."""
    _FIELDS = ('label', 'onset_s', 'offset_s', 'onset_sample', 'offset_sample')

    label = attr.ib(converter=str)
    onset_s = attr.ib(converter=attr.converters.optional(float_or_None))
    offset_s = attr.ib(converter=attr.converters.optional(float_or_None))
    onset_sample = attr.ib(converter=attr.converters.optional(int_or_None))
    offset_sample = attr.ib(converter=attr.converters.optional(int_or_None))
    asdict = attr.asdict

    @classmethod
    def from_row(cls, row, header=None):
        if type(row) is list:
            if header is None:
                raise ValueError(
                    'must provide header when row is a list'
                )
            row = dict(zip(header, row))
        elif type(row) is dict:
            if header is not None:
                warnings.warn(
                    "Type of 'row' argument was 'dict' but 'header'" 
                    "argument was not None. Value for header will not "
                    "be used because keys of dict are used as field from "
                    "header. To use a different header, convert row to a list: "
                    ">>> row = list(dict.values())"
                )

        row_dict = {}
        for field in cls._FIELDS:
            try:
                row_dict[field] = row[field]
            except KeyError:
                raise KeyError(
                    f'missing field {field} in row'
                )

        return cls.from_keyword(**row_dict)

    @classmethod
    def from_keyword(cls, label, onset_s=None, offset_s=None,
                     onset_sample=None, offset_sample=None):
        if ((onset_sample is None and offset_sample is None) and
                (onset_s is None and offset_s is None)):
            raise ValueError('must provide either onset_sample and offset_sample, or '
                             'onsets_s and offsets_s')

        if onset_sample and offset_sample is None:
            raise ValueError(f'onset_sample specified as {onset_sample} but offset_sample is None')
        if onset_sample is None and offset_sample:
            raise ValueError(f'offset_sample specified as {offset_sample} but onset_sample is None')
        if onset_s and offset_s is None:
            raise ValueError(f'onset_s specified as {onset_s} but offset_s is None')
        if onset_s is None and offset_s:
            raise ValueError(f'offset_s specified as {offset_sample} but onset_s is None')

        return cls(label=label, onset_s=onset_s, offset_s=offset_s,
                   onset_sample=onset_sample, offset_sample=offset_sample)
