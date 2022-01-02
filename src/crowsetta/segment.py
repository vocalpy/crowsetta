"""defines Segment class"""
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
    """object that represents a segment of a time series,
     usually a syllable in a bout of birdsong"""
    _FIELDS = ('label', 'onset_s', 'offset_s', 'onset_ind', 'offset_ind')

    label = attr.ib(converter=str)
    onset_s = attr.ib(converter=attr.converters.optional(float_or_None))
    offset_s = attr.ib(converter=attr.converters.optional(float_or_None))
    onset_ind = attr.ib(converter=attr.converters.optional(int_or_None))
    offset_ind = attr.ib(converter=attr.converters.optional(int_or_None))
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
                     onset_ind=None, offset_ind=None):
        if ((onset_ind is None and offset_ind is None) and
                (onset_s is None and offset_s is None)):
            raise ValueError('must provide either onset_ind and offset_ind, or '
                             'onsets_s and offsets_s')

        if onset_ind and offset_ind is None:
            raise ValueError(f'onset_ind specified as {onset_ind} but offset_ind is None')
        if onset_ind is None and offset_ind:
            raise ValueError(f'offset_ind specified as {offset_ind} but onset_ind is None')
        if onset_s and offset_s is None:
            raise ValueError(f'onset_s specified as {onset_s} but offset_s is None')
        if onset_s is None and offset_s:
            raise ValueError(f'offset_s specified as {offset_ind} but onset_s is None')

        return cls(label=label, onset_s=onset_s, offset_s=offset_s,
                   onset_ind=onset_ind, offset_ind=offset_ind)
