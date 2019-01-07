"""defines Segment class"""
import attr


@attr.s(frozen=True)
class Segment(object):
    """object that represents a segment of a time series,
     usually a syllable in a bout of birdsong"""
    _FIELDS = ('label', 'onset_s', 'offset_s', 'onset_Hz', 'offset_Hz', 'file')

    label = attr.ib(converter=str)
    file = attr.ib(converter=str)
    onset_s = attr.ib(converter=attr.converters.optional(float))
    offset_s = attr.ib(converter=attr.converters.optional(float))
    onset_Hz = attr.ib(converter=attr.converters.optional(int))
    offset_Hz = attr.ib(converter=attr.converters.optional(int))
    asdict = attr.asdict

    @classmethod
    def from_row(cls, row, header):
        row_dict = dict(zip(header, row))
        return cls.from_keyword(**row_dict)

    @classmethod
    def from_keyword(cls, label, file, onset_s=None, offset_s=None,
                     onset_Hz=None, offset_Hz=None):
        if ((onset_Hz is None and offset_Hz is None) and
                (onset_s is None and offset_s is None)):
            raise ValueError('must provide either onset_Hz and offset_Hz, or '
                             'onsets_s and offsets_s')

        if onset_Hz and offset_Hz is None:
            raise ValueError(f'onset_Hz specified as {onset_Hz} but offset_Hz is None')
        if onset_Hz is None and offset_Hz:
            raise ValueError(f'offset_Hz specified as {offset_Hz} but onset_Hz is None')
        if onset_s and offset_s is None:
            raise ValueError(f'onset_s specified as {onset_s} but offset_s is None')
        if onset_s is None and offset_s:
            raise ValueError(f'offset_s specified as {offset_Hz} but onset_s is None')

        return cls(label=label, file=file, onset_s=onset_s, offset_s=offset_s, 
                   onset_Hz=onset_Hz, offset_Hz=offset_Hz)
