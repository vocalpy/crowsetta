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
    onset_inds : numpy.ndarray or None
        of type int, onset of each annotated segment in samples/second
    offset_inds : numpy.ndarray or None
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
                 onset_inds=None,
                 offset_inds=None):
        """Sequence __init__

        Parameters
        ----------
        segments : list or tuple
            of Segment objects.
        onset_inds : numpy.ndarray or None
            of type int, onset of each annotated segment in samples/second
        offset_inds : numpy.ndarray or None
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
         onset_inds,
         offset_inds,
         labels) = self._validate_onsets_offsets_labels(onsets_s,
                                                        offsets_s,
                                                        onset_inds,
                                                        offset_inds,
                                                        labels)

        self._validate_segments_type(segments)

        super().__setattr__('_segments', segments)
        super().__setattr__('_onsets_s', onsets_s)
        super().__setattr__('_offsets_s', offsets_s)
        super().__setattr__('_onset_inds', onset_inds)
        super().__setattr__('_offset_inds', offset_inds)
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
    def onset_inds(self):
        return self._onset_inds

    @property
    def offset_inds(self):
        return self._offset_inds

    @property
    def labels(self):
        return self._labels

    def __hash__(self):
        list_for_hash = [self._segments,
                         self._onsets_s,
                         self._offsets_s,
                         self._onset_inds,
                         self._offset_inds,
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
                     '_onset_inds', '_offset_inds']:
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
                                        onset_inds,
                                        offset_inds,
                                        labels):
        """validate onsets, offsets, and labels passed to __init__ or class methods

        Parameters
        ----------
        onsets_s : numpy.ndarray or None
        offsets_s : numpy.ndarray or None
        onset_inds : numpy.ndarray or None
        offset_inds : numpy.ndarray or None
        labels : str, list, or tuple

        Returns
        -------
        onsets_s : numpy.ndarray
        offsets_s : numpy.ndarray
        onset_inds : numpy.ndarray
        offset_inds : numpy.ndarray
        labels : numpy.ndarray 
        """
        # make sure user passed either onset_inds and offset_inds, or
        # onsets_s and offsets_s, or both.
        # first make sure at least one pair of onsets and offsets is specified
        if ((onset_inds is None and offset_inds is None) and
                (onsets_s is None and offsets_s is None)):
            raise ValueError('must provide either onset_inds and offset_inds, or '
                             'onsets_s and offsets_s')

        # then make sure both elements of each pair are specified
        if onset_inds is not None and offset_inds is None:
            raise ValueError(f'onset_ind specified as {onset_inds} but offset_ind is None')
        if onset_inds is None and offset_inds is not None:
            raise ValueError(f'offset_ind specified as {offset_inds} but onset_ind is None')
        if onsets_s is not None and offsets_s is None:
            raise ValueError(f'onset_s specified as {onsets_s} but offset_s is None')
        if onsets_s is None and offsets_s is not None:
            raise ValueError(f'offset_s specified as {offset_inds} but onset_s is None')

        # then do type/shape checking on onsets and offsets;
        # also make sure everybody is the same length
        if (not (onset_inds is None and offset_inds is None) and
           not (np.all(onset_inds == None) and np.all(offset_inds == None))):
            onset_inds = column_or_row_or_1d(onset_inds)
            offset_inds = column_or_row_or_1d(offset_inds)

            if onset_inds.dtype != int or offset_inds.dtype != int:
                raise TypeError('dtype of onset_inds and offset_inds '
                                'must be some kind of int')

            try:
                check_consistent_length([labels, onset_inds, offset_inds])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onset_inds.shape[0] == offset_inds.shape[0]):
                    raise ValueError('onset_inds and offset_inds have different lengths: '
                                     f'labels: {onset_inds.shape[0]}, '
                                     f'onset_inds: {offset_inds.shape[0]}')
                if not (labels.shape[0] == onset_inds.shape[0]):
                    raise ValueError('labels and onset_inds have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onset_inds: {onset_inds.shape[0]}')
                if not (labels.shape[0] == offset_inds.shape[0]):
                    raise ValueError('labels and offset_inds have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onset_inds: {offset_inds.shape[0]}')

        if (not (onsets_s is None and offsets_s is None) and
           not (np.all(onsets_s == None) and np.all(offsets_s == None))):
            onsets_s = column_or_row_or_1d(onsets_s)
            offsets_s = column_or_row_or_1d(offsets_s)

            if onsets_s.dtype != float or offsets_s.dtype != float:
                raise TypeError('dtype of onsets_s and offsets_s '
                                'must be some kind of float')

            try:
                check_consistent_length([labels, onset_inds, offset_inds])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onsets_s.shape[0] == offsets_s.shape[0]):
                    raise ValueError('onset_inds and offset_inds have different lengths: '
                                     f'labels: {onsets_s.shape[0]}, '
                                     f'onset_inds: {offsets_s.shape[0]}')
                if not (labels.shape[0] == onsets_s.shape[0]):
                    raise ValueError('labels and onsets_s have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onset_inds: {onset_inds.shape[0]}')
                if not (labels.shape[0] == offset_inds.shape[0]):
                    raise ValueError('labels and offset_inds have different lengths: '
                                     f'labels: {labels.shape[0]}, '
                                     f'onset_inds: {offset_inds.shape[0]}')

        num_samples = _num_samples(labels)

        # need to make arrays to iterate over for onsets and offsets that are None
        if onset_inds is None and offset_inds is None:
            onset_inds = np.asarray([None] * num_samples)
            offset_inds = np.asarray([None] * num_samples)
        elif onsets_s is None and offsets_s is None:
            onsets_s = np.asarray([None] * num_samples)
            offsets_s = np.asarray([None] * num_samples)

        return onsets_s, offsets_s, onset_inds, offset_inds, labels

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
        onset_inds = []
        offset_inds = []
        labels = []

        for seg in segments:
            onsets_s.append(seg.onset_s)
            offsets_s.append(seg.offset_s)
            onset_inds.append(seg.onset_ind)
            offset_inds.append(seg.offset_ind)
            labels.append(seg.label)

        onsets_s = np.asarray(onsets_s)
        offsets_s = np.asarray(offsets_s)
        onset_inds = np.asarray(onset_inds)
        offset_inds = np.asarray(offset_inds)
        labels = np.asarray(labels)

        labels = cls._convert_labels(labels)

        (onsets_s,
         offsets_s,
         onset_inds,
         offset_inds,
         labels) = cls._validate_onsets_offsets_labels(onsets_s,
                                                       offsets_s,
                                                       onset_inds,
                                                       offset_inds,
                                                       labels)

        return cls(segments,
                   labels,
                   onsets_s,
                   offsets_s,
                   onset_inds,
                   offset_inds)

    @classmethod
    def from_keyword(cls, labels, onset_inds=None, offset_inds=None,
                     onsets_s=None, offsets_s=None):
        """construct a Sequence from keyword arguments

        Parameters
        ----------
        onset_inds : numpy.ndarray or None
            of type int, onset of each annotated segment in samples/second
        offset_inds : numpy.ndarray or None
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
         onset_inds,
         offset_inds,
         labels) = cls._validate_onsets_offsets_labels(onsets_s,
                                                       offsets_s,
                                                       onset_inds,
                                                       offset_inds,
                                                       labels)

        segments = []
        zipped = zip(labels, onset_inds, offset_inds, onsets_s, offsets_s)
        for label, onset_ind, offset_ind, onset_s, offset_s in zipped:
            segments.append(Segment.from_keyword(label=label,
                                                 onset_ind=onset_ind,
                                                 offset_ind=offset_ind,
                                                 onset_s=onset_s,
                                                 offset_s=offset_s))

        return cls(segments,
                   labels,
                   onsets_s,
                   offsets_s,
                   onset_inds,
                   offset_inds
                   )

    @classmethod
    def from_dict(cls, seq_dict):
        """returns a Sequence, given a Python dictionary
        where keys of dictionary are arguments to Sequence.from_keyword()

        Parameters
        ----------
        seq_dict : dict
            with following key, value pairs
            onset_inds : numpy.ndarray or None
                of type int, onset of each annotated segment in samples/second
            offset_inds : numpy.ndarray or None
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
        ...     'onset_inds': np.asarray([16005, 17925, 19837]),
        ...     'offset_inds': np.asarray([17602, 19520, 21435]),
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
                onset_inds : numpy.ndarray or None
                    of type int, onset of each annotated segment in samples/second
                offset_inds : numpy.ndarray or None
                    of type int, offset of each annotated segment in samples/second
                onsets_s : numpy.ndarray or None
                    of type float, onset of each annotated segment in seconds
                offsets_s : numpy.ndarray or None
                    of type float, offset of each annotated segment in seconds
                labels : numpy.ndarray
                    of type str; label for each annotated segment
        """
        seq_keys = ['onset_inds', 'offset_inds', 'onsets_s', 'offsets_s', 'labels']
        seq_dict = dict(zip(
            seq_keys, [getattr(self, seq_key) for seq_key in seq_keys]
        ))

        for a_key in ['onset_inds', 'offset_inds', 'onsets_s', 'offsets_s']:
            # if value is an array full of Nones, just convert to one None.
            # Use == to do elementwise comparison (so ignore warnings about
            # 'comparison with None performed with equality operators')
            if np.all(seq_dict[a_key] == None):
                seq_dict[a_key] = None

        return seq_dict
