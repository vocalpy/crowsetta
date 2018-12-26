"""defines Segment and Sequence classes used for conversion"""
import attr
import numpy as np

from .validation import _num_samples, check_consistent_length, column_or_1d


@attr.s
class Segment(object):
    """object that represents a segment of a time series,
     usually a syllable in a bout of birdsong"""
    label = attr.ib(converter=str)
    onset_s = attr.ib(converter=attr.converters.optional(float))
    offset_s = attr.ib(converter=attr.converters.optional(float))
    onset_Hz = attr.ib(converter=attr.converters.optional(int))
    offset_Hz = attr.ib(converter=attr.converters.optional(int))
    file = attr.ib(converter=str)
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


class SegmentList(list):
    """represents an ordered list of Segment instances.
    Used for segments attribute of Sequence class.
    Subclasses a list to override the __repr__ method, basically so user gets
    newlines after every Segment, making it hopefully easier to read.
    """
    def __init__(self, segments):
        super().__init__()
        self.segments = segments

    def __repr__(self):
        segments_str = '\n'.join([str(segment) for segment in self.segments])
        return '<SegmentList(\n' + segments_str + '\n)>'

    @classmethod
    def from_list_or_tuple(cls, segments):
        if type(segments) != list and type(segments) != tuple:
            raise TypeError(f'Unable to create list of segments from a {type(segments)}')
        if not all([type(segment) == Segment for segment in segments]):
            raise TypeError('all items in segments must be of type Segment')
        return cls(segments)


@attr.s
class Sequence:
    """object that represents a sequence of segments, such as a bout of birdsong made
    up of syllables
    """
    segments = attr.ib(converter=SegmentList.from_list_or_tuple)

    @classmethod
    def from_segments(cls, segments):
        return cls(segments)

    @classmethod
    def from_keyword(cls, file, labels, onsets_Hz=None, offsets_Hz=None,
                     onsets_s=None, offsets_s=None):
        """construct a Sequence from keyword arguments

        Parameters
        ----------
        file : str
            name of audio file with which annotation is associated.
        onsets_Hz : numpy.ndarray or None
            of type int, onset of each annotated segment in samples/second
        offsets_Hz : numpy.ndarray or None
            of type int, offset of each annotated segment in samples/second
        onsets_s : numpy.ndarray or None
            of type float, onset of each annotated segment in seconds
        offsets_s : numpy.ndarray or None
            of type float, offset of each annotated segment in seconds
        labels : str, list, or numpy.ndarray
            of type str, label for each annotated segment

        Must specify both onsets and offsets, either in units of Hz or seconds (or both).
        """
        if type(labels) not in (str, list, tuple, np.ndarray):
            raise TypeError('labels arguments must be a string, list, tuple, or numpy '
                            f'array, not {type(labels)}')

        if type(labels) == str:
            labels = np.asarray(list(labels))
        elif type(labels) == list or type(labels) == tuple:
            try:
                labels = [str(label) for label in labels]
            except ValueError:
                raise ValueError('unable to convert all elements in labels to characters')
            labels = np.asarray(labels)

        # make sure user passed either onsets_Hz and offsets_Hz, or
        # onsets_s and offsets_s, or both.
        # first make sure at least one pair of onsets and offsets is specified
        if ((onsets_Hz is None and offsets_Hz is None) and
                (onsets_s is None and offsets_s is None)):
            raise ValueError('must provide either onsets_Hz and offsets_Hz, or '
                             'onsets_s and offsets_s')

        # then make sure both elements of each pair are specified
        if onsets_Hz is not None and offsets_Hz is None:
            raise ValueError(f'onset_Hz specified as {onsets_Hz} but offset_Hz is None')
        if onsets_Hz is None and offsets_Hz is not None:
            raise ValueError(f'offset_Hz specified as {offsets_Hz} but onset_Hz is None')
        if onsets_s is not None and offsets_s is None:
            raise ValueError(f'onset_s specified as {onsets_s} but offset_s is None')
        if onsets_s is None and offsets_s is not None:
            raise ValueError(f'offset_s specified as {offsets_Hz} but onset_s is None')

        # then do type/shape checking on onsets and offsets;
        # also make sure everybody is the same length
        if onsets_Hz is not None and offsets_Hz is not None:
            onsets_Hz = column_or_1d(onsets_Hz)
            offsets_Hz = column_or_1d(offsets_Hz)

            if onsets_Hz.dtype != int or offsets_Hz.dtype != int:
                raise TypeError('dtype of onsets_Hz and offsets_Hz '
                                'must be some kind of int')

            try:
                check_consistent_length([labels, onsets_Hz, offsets_Hz])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onsets_Hz.shape[0] == offsets_Hz.shape[0]):
                    raise ValueError('onsets_Hz and offsets_Hz have different lengths: '
                                     f'labels: {onsets_Hz.shape[0]}, '
                                     f'onsets_Hz: {offsets_Hz.shape[0]}')
                if not (labels.shape[0] == onsets_Hz.shape[0]):
                    raise ValueError('labels and onsets_Hz have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onsets_Hz: {onsets_Hz.shape[0]}')
                if not (labels.shape[0] == offsets_Hz.shape[0]):
                    raise ValueError('labels and offsets_Hz have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onsets_Hz: {offsets_Hz.shape[0]}')

        if onsets_s is not None and offsets_s is not None:
            onsets_s = column_or_1d(onsets_s)
            offsets_s = column_or_1d(offsets_s)

            if onsets_s.dtype != float or offsets_s.dtype != float:
                raise TypeError('dtype of onsets_s and offsets_s '
                                'must be some kind of float')

            try:
                check_consistent_length([labels, onsets_Hz, offsets_Hz])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onsets_s.shape[0] == offsets_s.shape[0]):
                    raise ValueError('onsets_Hz and offsets_Hz have different lengths: '
                                     f'labels: {onsets_s.shape[0]}, '
                                     f'onsets_Hz: {offsets_s.shape[0]}')
                if not (labels.shape[0] == onsets_s.shape[0]):
                    raise ValueError('labels and onsets_s have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onsets_Hz: {onsets_Hz.shape[0]}')
                if not (labels.shape[0] == offsets_Hz.shape[0]):
                    raise ValueError('labels and offsets_Hz have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onsets_Hz: {offsets_Hz.shape[0]}')

        num_samples = _num_samples(labels)

        # need to make arrays to iterate over for onsets and offsets that are None
        if onsets_Hz is None and offsets_Hz is None:
            onsets_Hz = np.asarray([None] * num_samples)
            offsets_Hz = np.asarray([None] * num_samples)
        elif onsets_s is None and offsets_s is None:
            onsets_s = np.asarray([None] * num_samples)
            offsets_s = np.asarray([None] * num_samples)

        segments = []
        zipped = zip(labels, onsets_Hz, offsets_Hz, onsets_s, offsets_s)
        for label, onset_Hz, offset_Hz, onset_s, offset_s in zipped:
            segments.append(Segment.from_keyword(label=label,
                                                 onset_Hz=onset_Hz,
                                                 offset_Hz=offset_Hz,
                                                 onset_s=onset_s,
                                                 offset_s=offset_s,
                                                 file=file)
                            )
        return cls.from_segments(segments)

    @classmethod
    def from_dict(cls, annot_dict):
        """returns a Sequence, given a Python dictionary
        where keys of dictionary are arguments to Sequence.from_keyword()

        Parameters
        ----------
        annot_dict : dict
            with following key, value pairs
            file : str
                name of audio file with which annotation is associated.
            onsets_Hz : numpy.ndarray or None
                of type int, onset of each annotated segment in samples/second
            offsets_Hz : numpy.ndarray or None
                of type int, offset of each annotated segment in samples/second
            onsets_s : numpy.ndarray or None
                of type float, onset of each annotated segment in seconds
            offsets_s : numpy.ndarray or None
                of type float, offset of each annotated segment in seconds
            labels : str, list, or numpy.ndarray
                of type str, label for each annotated segment

        annot_dict must specify both onsets and offsets, either in units of Hz or seconds 
        (or both).

        Examples
        --------
        >>> annot_dict = {
        ...     'labels': 'abc',
        ...     'onsets_Hz': np.asarray([16005, 17925, 19837]),
        ...     'offsets_Hz': np.asarray([17602, 19520, 21435]),
        ...     'file': 'bird0.wav',
        ...     }
        >>> seq = Sequence.from_dict(annot_dict)
        """
        # basically a convenience method
        # so user doesn't have to grok the concept of 'dictionary unpacking operator'
        return cls.from_keyword(**annot_dict)
