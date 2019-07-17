"""defines Sequence class"""
import numpy as np

from .validation import _num_samples, check_consistent_length, column_or_row_or_1d 

from .segment import Segment


class Sequence:
    """object that represents a sequence of segments, such as a bout of birdsong made
    up of syllables

    Attributes
    ----------
    segments : tuple
        of Segment objects.
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

    Methods
    -------
    from_segments : make a Sequence from a list of segments
    from_keyword : make a Sequence by passing keywords (all arguments except segments)
    from_dict : like from_keyword, but pass a Python dictionary where keys are keywords
        and values are arguments for those keywords
    to_dict : convert to a dict. The inverse of from_dict.
    """
    def __init__(self,
                 segments,
                 labels,
                 onsets_s=None,
                 offsets_s=None,
                 onsets_Hz=None,
                 offsets_Hz=None):
        """Sequence __init__

        Parameters
        ----------
        segments : list or tuple
            of Segment objects.
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
        """
        if segments is not None:
            if type(segments) == Segment:
                segments = (segments,)
            elif type(segments) in (list, tuple):
                segments = tuple(segments)
            else:
                raise TypeError(
                    f"type of 'segments' should be either list, tuple, or a single segment but "
                    f"got type {type(segments)}, could not convert to tuple."
                )

        labels = self._convert_labels(labels)

        (onsets_s,
         offsets_s,
         onsets_Hz,
         offsets_Hz,
         labels) = self._validate_onsets_offsets_labels(onsets_s,
                                                        offsets_s,
                                                        onsets_Hz,
                                                        offsets_Hz,
                                                        labels)

        self._validate_segments_type(segments)

        super().__setattr__('_segments', segments)
        super().__setattr__('_onsets_s', onsets_s)
        super().__setattr__('_offsets_s', offsets_s)
        super().__setattr__('_onsets_Hz', onsets_Hz)
        super().__setattr__('_offsets_Hz', offsets_Hz)
        super().__setattr__('_labels', labels)

    @property
    def segments(self):
        return self._segments

    @property
    def onsets_s(self):
        return self._onsets_s

    @property
    def offsets_s(self):
        return self._offsets_s

    @property
    def onsets_Hz(self):
        return self._onsets_Hz

    @property
    def offsets_Hz(self):
        return self._offsets_Hz

    @property
    def labels(self):
        return self._labels

    def __hash__(self):
        list_for_hash = [self._segments,
                         self._onsets_s,
                         self._offsets_s,
                         self._onsets_Hz,
                         self._offsets_Hz,
                         self._labels]
        list_for_hash = [tuple(item.tolist())
                         if type(item) == np.ndarray
                         else item
                         for item in list_for_hash
                         ]
        tup_for_hash = tuple(list_for_hash)
        return hash(tup_for_hash)

    def __repr__(self):
        return f"<Sequence with {len(self.segments)} segments>"

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False

        eq = []
        for attr in ['_segments', '_labels', '_onsets_s', '_offsets_s',
                     '_onsets_Hz', '_offsets_Hz']:
            self_attr = getattr(self, attr)
            other_attr = getattr(other, attr)
            if type(self_attr) == np.ndarray:
                eq.append(np.array_equal(self_attr, other_attr))
            else:
                eq.append(self_attr == other_attr)

        if all(eq):
            return True
        else:
            return False

    def __ne__(self, other):
        if self.__class__ == other.__class__:
            return not self.__eq__(other)
        else:
            raise TypeError("can only test for equality between two Sequences, not "
                            f"between a Sequence and {type(other)}")

    def __setattr__(self, key, value):
        raise TypeError('Sequence objects are immutable.')

    def __lt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    @staticmethod
    def _convert_labels(labels):
        if type(labels) == str:
            labels = np.asarray(list(labels))
        elif type(labels) == list or type(labels) == tuple:
            try:
                labels = [str(label) for label in labels]
            except ValueError:
                raise ValueError('unable to convert all elements in labels to characters')
            labels = np.asarray(labels)
        return labels

    @staticmethod
    def _validate_segments_type(segments):
        """validate that all items in list of segments are Segment"""
        if not all([type(seg) == Segment for seg in segments]):
            raise TypeError(
                'A Sequence must be made from a list of Segments but not all '
                'items in the list passed were Segments.')

    @staticmethod
    def _validate_onsets_offsets_labels(onsets_s,
                                        offsets_s,
                                        onsets_Hz,
                                        offsets_Hz,
                                        labels):
        """validate onsets, offsets, and labels passed to __init__ or class methods

        Parameters
        ----------
        onsets_s : numpy.ndarray or None
        offsets_s : numpy.ndarray or None
        onsets_Hz : numpy.ndarray or None
        offsets_Hz : numpy.ndarray or None
        labels : str, list, or tuple

        Returns
        -------
        onsets_s : numpy.ndarray
        offsets_s : numpy.ndarray
        onsets_Hz : numpy.ndarray
        offsets_Hz : numpy.ndarray
        labels : numpy.ndarray 
        """
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
        if (not (onsets_Hz is None and offsets_Hz is None) and
           not (np.all(onsets_Hz == None) and np.all(offsets_Hz == None))):
            onsets_Hz = column_or_row_or_1d(onsets_Hz)
            offsets_Hz = column_or_row_or_1d(offsets_Hz)

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

        if (not (onsets_s is None and offsets_s is None) and
           not (np.all(onsets_s == None) and np.all(offsets_s == None))):
            onsets_s = column_or_row_or_1d(onsets_s)
            offsets_s = column_or_row_or_1d(offsets_s)

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

        return onsets_s, offsets_s, onsets_Hz, offsets_Hz, labels

    @classmethod
    def from_segments(cls, segments):
        """construct a Sequence from a list of Segment objects

        Parameters
        ----------
        segments

        Returns
        -------
        seq : Sequence
            instance of Sequence generated using list of segments
        """
        cls._validate_segments_type(segments)

        onsets_s = []
        offsets_s = []
        onsets_Hz = []
        offsets_Hz = []
        labels = []

        for seg in segments:
            onsets_s.append(seg.onset_s)
            offsets_s.append(seg.offset_s)
            onsets_Hz.append(seg.onset_Hz)
            offsets_Hz.append(seg.offset_Hz)
            labels.append(seg.label)

        onsets_s = np.asarray(onsets_s)
        offsets_s = np.asarray(offsets_s)
        onsets_Hz = np.asarray(onsets_Hz)
        offsets_Hz = np.asarray(offsets_Hz)
        labels = np.asarray(labels)

        labels = cls._convert_labels(labels)

        (onsets_s,
         offsets_s,
         onsets_Hz,
         offsets_Hz,
         labels) = cls._validate_onsets_offsets_labels(onsets_s,
                                                       offsets_s,
                                                       onsets_Hz,
                                                       offsets_Hz,
                                                       labels)

        return cls(segments,
                   labels,
                   onsets_s,
                   offsets_s,
                   onsets_Hz,
                   offsets_Hz)

    @classmethod
    def from_keyword(cls, labels, onsets_Hz=None, offsets_Hz=None,
                     onsets_s=None, offsets_s=None):
        """construct a Sequence from keyword arguments

        Parameters
        ----------
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
        labels = cls._convert_labels(labels)

        (onsets_s,
         offsets_s,
         onsets_Hz,
         offsets_Hz,
         labels) = cls._validate_onsets_offsets_labels(onsets_s,
                                                       offsets_s,
                                                       onsets_Hz,
                                                       offsets_Hz,
                                                       labels)

        segments = []
        zipped = zip(labels, onsets_Hz, offsets_Hz, onsets_s, offsets_s)
        for label, onset_Hz, offset_Hz, onset_s, offset_s in zipped:
            segments.append(Segment.from_keyword(label=label,
                                                 onset_Hz=onset_Hz,
                                                 offset_Hz=offset_Hz,
                                                 onset_s=onset_s,
                                                 offset_s=offset_s))

        return cls(segments,
                   labels,
                   onsets_s,
                   offsets_s,
                   onsets_Hz,
                   offsets_Hz
                   )

    @classmethod
    def from_dict(cls, seq_dict):
        """returns a Sequence, given a Python dictionary
        where keys of dictionary are arguments to Sequence.from_keyword()

        Parameters
        ----------
        seq_dict : dict
            with following key, value pairs
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

        seq_dict must specify both onsets and offsets, either in units of Hz or seconds
        (or both).

        Examples
        --------
        >>> seq_dict = {
        ...     'labels': 'abc',
        ...     'onsets_Hz': np.asarray([16005, 17925, 19837]),
        ...     'offsets_Hz': np.asarray([17602, 19520, 21435]),
        ...     'file': 'bird0.wav',
        ...     }
        >>> seq = Sequence.from_dict(seq_dict)
        """
        # basically a convenience method
        # so user doesn't have to grok the concept of 'dictionary unpacking operator'
        return cls.from_keyword(**seq_dict)

    def as_dict(self):
        """returns sequence as a dictionary

        Parameters
        ----------
        None

        Returns
        -------
        seq_dict : dict
            with the following key, value pairs:
                onsets_Hz : numpy.ndarray or None
                    of type int, onset of each annotated segment in samples/second
                offsets_Hz : numpy.ndarray or None
                    of type int, offset of each annotated segment in samples/second
                onsets_s : numpy.ndarray or None
                    of type float, onset of each annotated segment in seconds
                offsets_s : numpy.ndarray or None
                    of type float, offset of each annotated segment in seconds
                labels : numpy.ndarray
                    of type str; label for each annotated segment
        """
        seq_keys = ['onsets_Hz', 'offsets_Hz', 'onsets_s', 'offsets_s', 'labels']
        seq_dict = dict(zip(
            seq_keys, [getattr(self, seq_key) for seq_key in seq_keys]
        ))

        for a_key in ['onsets_Hz', 'offsets_Hz', 'onsets_s', 'offsets_s']:
            # if value is an array full of Nones, just convert to one None.
            # Use == to do elementwise comparison (so ignore warnings about
            # 'comparison with None performed with equality operators')
            if np.all(seq_dict[a_key] == None):
                seq_dict[a_key] = None

        return seq_dict
