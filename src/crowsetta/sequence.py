"""A class that represents a sequence of segments,
used to annotate animal acoustic communication."""

from __future__ import annotations

import numpy as np

from .segment import Segment
from .validation import _num_samples, check_consistent_length, column_or_row_or_1d


class Sequence:
    """A class that represents a sequence of segments,
    used to annotate animal acoustic communication.

    E.g., a human sentence made up of syllables,
    or a bout of birdsong made up of "syllables".

    Attributes
    ----------
    segments : tuple
        A :class:`tuple` of :class:`crowsetta.Segment` instances.
    onset_samples : numpy.ndarray or None
        Numpy array of type int, onset of each annotated segment in sample number.
    offset_samples : numpy.ndarray or None
        Numpy array of type int, offset of each annotated segment in sample number.
    onsets_s : numpy.ndarray or None
        Numpy array of type float, onset of each annotated segment in seconds.
    offsets_s : numpy.ndarray or None
        Numpy array of type float, offset of each annotated segment in seconds.
    labels : str, list, or numpy.ndarray
        Numpy array of type char, label for each annotated segment.

    Methods
    -------
    from_segments : method
        Make a :class:`~crowsetta.Sequence` from a :class:`list` of :class:`~crowsetta.Segment`s.
    from_keyword : method
        Make a :class:`~crowsetta.Sequence` by passing keywords (all arguments except segments)
    from_dict : method
        Like from_keyword, but pass a Python dictionary where keys are keywords
        and values are arguments for those keywords.
    to_dict : method
        Convert to a :class:`dict`. The inverse of :meth:`~crowsetta.Sequence.from_dict`.

    Examples
    --------

    A sequence with onsets and offsets given in seconds.

    >>> import numpy as np
    >>> import crowsetta
    >>> onsets_s = np.array([1.0, 3.0, 5.0])
    >>> offsets_s = np.array(2.0, 4.0, 6.0])
    >>> labels = np.array(['a', 'a', 'b'])
    >>> seq = crowsetta.Sequence.from_keyword(labels=labels, onsets_s=onsets_s, offsets_s=offsets_s)

    The same sequence could also be made
    by calling the :meth:`~crowsetta.Sequence.from_segments` class method.

    >>> segments = []
    >>> for onset, offset, label in zip(onsets_s, offsets_s, labels):
    ...     segments.append(crowsetta.Segment(onset_s=onset, offset_s=offset, label=label))
    >>> seq2 = crowsetta.Sequence.from_segments(segments)
    """

    def __init__(self, segments, labels, onsets_s=None, offsets_s=None, onset_samples=None, offset_samples=None):
        """Initialize a new :class:`~crowsetta.Sequence` instance.

        Parameters
        ----------
        segments : tuple
            A :class:`tuple` of :class:`crowsetta.Segment` instances.
        onset_samples : numpy.ndarray or None
            Numpy array of type int, onset of each annotated segment in sample number.
        offset_samples : numpy.ndarray or None
            Numpy array of type int, offset of each annotated segment in sample number.
        onsets_s : numpy.ndarray or None
            Numpy array of type float, onset of each annotated segment in seconds.
        offsets_s : numpy.ndarray or None
            Numpy array of type float, offset of each annotated segment in seconds.
        labels : str, list, or numpy.ndarray
            Numpy array of type char, label for each annotated segment.
        """
        if segments is not None:
            if isinstance(segments, Segment):
                segments = (segments,)
            elif isinstance(segments, (list, tuple)):
                segments = tuple(segments)
            else:
                raise TypeError(
                    f"type of 'segments' should be either list, tuple, or a single segment but "
                    f"got type {type(segments)}, could not convert to tuple."
                )

        labels = self._convert_labels(labels)

        (onsets_s, offsets_s, onset_samples, offset_samples, labels) = self._validate_onsets_offsets_labels(
            onsets_s, offsets_s, onset_samples, offset_samples, labels
        )

        self._validate_segments_type(segments)

        super().__setattr__("_segments", segments)
        super().__setattr__("_onsets_s", onsets_s)
        super().__setattr__("_offsets_s", offsets_s)
        super().__setattr__("_onset_samples", onset_samples)
        super().__setattr__("_offset_samples", offset_samples)
        super().__setattr__("_labels", labels)

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
    def onset_samples(self):
        return self._onset_samples

    @property
    def offset_samples(self):
        return self._offset_samples

    @property
    def labels(self):
        return self._labels

    def __hash__(self):
        list_for_hash = [
            self._segments,
            self._onsets_s,
            self._offsets_s,
            self._onset_samples,
            self._offset_samples,
            self._labels,
        ]
        list_for_hash = [tuple(item.tolist()) if isinstance(item, np.ndarray) else item for item in list_for_hash]
        tup_for_hash = tuple(list_for_hash)
        return hash(tup_for_hash)

    def __repr__(self):
        return f"<Sequence with {len(self.segments)} segments>"

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False

        if len(self.segments) != len(other.segments):
            return False

        return all([seg1 == seg2 for seg1, seg2 in zip(self.segments, other.segments)])

    def __ne__(self, other):
        if self.__class__ == other.__class__:
            return not self.__eq__(other)
        else:
            raise TypeError(
                "can only test for equality between two Sequences, not " f"between a Sequence and {type(other)}"
            )

    def __setattr__(self, key, value):
        raise TypeError("Sequence objects are immutable.")

    def __lt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __len__(self):
        return self.onsets_s.shape[-1]

    @staticmethod
    def _convert_labels(labels):
        if isinstance(labels, str):
            labels = np.asarray(list(labels))
        elif isinstance(labels, list) or isinstance(labels, tuple):
            try:
                labels = [str(label) for label in labels]
            except ValueError:
                raise ValueError("unable to convert all elements in labels to characters")
            labels = np.asarray(labels)
        return labels

    @staticmethod
    def _validate_segments_type(segments):
        """Validate that all items in list of segments are Segment"""
        if not all([isinstance(seg, Segment) for seg in segments]):
            raise TypeError(
                "A Sequence must be made from a list of Segments but not all " "items in the list passed were Segments."
            )

    @staticmethod
    def _validate_onsets_offsets_labels(onsets_s, offsets_s, onset_samples, offset_samples, labels):
        """Validate onsets, offsets, and labels passed to __init__ or class methods

        Parameters
        ----------
        onsets_s : numpy.ndarray or None
        offsets_s : numpy.ndarray or None
        onset_samples : numpy.ndarray or None
        offset_samples : numpy.ndarray or None
        labels : str, list, or tuple

        Returns
        -------
        onsets_s : numpy.ndarray
        offsets_s : numpy.ndarray
        onset_samples : numpy.ndarray
        offset_samples : numpy.ndarray
        labels : numpy.ndarray
        """
        # make sure user passed either onset_samples and offset_samples, or
        # onsets_s and offsets_s, or both.
        # first make sure at least one pair of onsets and offsets is specified
        if (onset_samples is None and offset_samples is None) and (onsets_s is None and offsets_s is None):
            raise ValueError("must provide either onset_samples and offset_samples, or " "onsets_s and offsets_s")

        # then make sure both elements of each pair are specified
        if onset_samples is not None and offset_samples is None:
            raise ValueError(f"onset_sample specified as {onset_samples} but offset_sample is None")
        if onset_samples is None and offset_samples is not None:
            raise ValueError(f"offset_sample specified as {offset_samples} but onset_sample is None")
        if onsets_s is not None and offsets_s is None:
            raise ValueError(f"onset_s specified as {onsets_s} but offset_s is None")
        if onsets_s is None and offsets_s is not None:
            raise ValueError(f"offset_s specified as {offset_samples} but onset_s is None")

        # then do type/shape checking on onsets and offsets;
        # also make sure everybody is the same length
        if not (onset_samples is None and offset_samples is None) and not (
            np.all(onset_samples == None) and np.all(offset_samples == None)  # noqa: E711
        ):
            onset_samples = column_or_row_or_1d(onset_samples)
            offset_samples = column_or_row_or_1d(offset_samples)

            if not np.issubdtype(onset_samples.dtype, np.integer) or not np.issubdtype(
                offset_samples.dtype, np.integer
            ):
                raise TypeError("dtype of onset_samples and offset_samples " "must be some kind of int")

            try:
                check_consistent_length([labels, onset_samples, offset_samples])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onset_samples.shape[0] == offset_samples.shape[0]):
                    raise ValueError(
                        "onset_samples and offset_samples have different lengths: "
                        f"labels: {onset_samples.shape[0]}, "
                        f"onset_samples: {offset_samples.shape[0]}"
                    )
                if not (labels.shape[0] == onset_samples.shape[0]):
                    raise ValueError(
                        "labels and onset_samples have different lengths: "
                        f"labels: {labels.shape[0]}, "
                        f"onset_samples: {onset_samples.shape[0]}"
                    )
                if not (labels.shape[0] == offset_samples.shape[0]):
                    raise ValueError(
                        "labels and offset_samples have different lengths: "
                        f"labels: {labels.shape[0]}, "
                        f"onset_samples: {offset_samples.shape[0]}"
                    )

        if not (onsets_s is None and offsets_s is None) and not (
            np.all(onsets_s == None) and np.all(offsets_s == None)  # noqa: E711
        ):
            onsets_s = column_or_row_or_1d(onsets_s)
            offsets_s = column_or_row_or_1d(offsets_s)

            if not np.issubdtype(onsets_s.dtype, np.floating) or not np.issubdtype(offsets_s.dtype, np.floating):
                raise TypeError("dtype of onsets_s and offsets_s " "must be some kind of float")

            try:
                check_consistent_length([labels, onset_samples, offset_samples])
            except ValueError:
                # try to give human-interpretable-error message
                if not (onsets_s.shape[0] == offsets_s.shape[0]):
                    raise ValueError(
                        "onset_samples and offset_samples have different lengths: "
                        f"labels: {onsets_s.shape[0]}, "
                        f"onset_samples: {offsets_s.shape[0]}"
                    )
                if not (labels.shape[0] == onsets_s.shape[0]):
                    raise ValueError(
                        "labels and onsets_s have different lengths: "
                        f"labels: {labels.shape[0]}, "
                        f"onset_samples: {onset_samples.shape[0]}"
                    )
                if not (labels.shape[0] == offset_samples.shape[0]):
                    raise ValueError(
                        "labels and offset_samples have different lengths: "
                        f"labels: {labels.shape[0]}, "
                        f"onset_samples: {offset_samples.shape[0]}"
                    )

        num_samples = _num_samples(labels)

        # need to make arrays to iterate over for onsets and offsets that are None
        if onset_samples is None and offset_samples is None:
            onset_samples = np.asarray([None] * num_samples)
            offset_samples = np.asarray([None] * num_samples)
        elif onsets_s is None and offsets_s is None:
            onsets_s = np.asarray([None] * num_samples)
            offsets_s = np.asarray([None] * num_samples)

        return onsets_s, offsets_s, onset_samples, offset_samples, labels

    @classmethod
    def from_segments(cls, segments):
        """Construct a :class:`crowsetta.Sequence`
        from a :class:`list` of :class:`crowsetta.Segment` objects.

        Parameters
        ----------
        segments : list
            A :class:`list` of :class:`crowsetta.Segment` instances.

        Returns
        -------
        seq : crowsetta.Sequence
            A :class:`~crowsetta.Sequence` instance
            generated using the :class:`list` of :class:`~crowsetta.Segment`s.
        """
        cls._validate_segments_type(segments)

        onsets_s = []
        offsets_s = []
        onset_samples = []
        offset_samples = []
        labels = []

        for seg in segments:
            onsets_s.append(seg.onset_s)
            offsets_s.append(seg.offset_s)
            onset_samples.append(seg.onset_sample)
            offset_samples.append(seg.offset_sample)
            labels.append(seg.label)

        onsets_s = np.asarray(onsets_s)
        offsets_s = np.asarray(offsets_s)
        onset_samples = np.asarray(onset_samples)
        offset_samples = np.asarray(offset_samples)
        labels = np.asarray(labels)

        labels = cls._convert_labels(labels)

        (onsets_s, offsets_s, onset_samples, offset_samples, labels) = cls._validate_onsets_offsets_labels(
            onsets_s, offsets_s, onset_samples, offset_samples, labels
        )

        return cls(segments, labels, onsets_s, offsets_s, onset_samples, offset_samples)

    @classmethod
    def from_keyword(cls, labels, onset_samples=None, offset_samples=None, onsets_s=None, offsets_s=None):
        """Construct a :class:`crowsetta.Sequence` from keyword arguments

        Parameters
        ----------
        onset_samples : numpy.ndarray or None
            of type int, onset of each annotated segment in samples/second
        offset_samples : numpy.ndarray or None
            of type int, offset of each annotated segment in samples/second
        onsets_s : numpy.ndarray or None
            of type float, onset of each annotated segment in seconds
        offsets_s : numpy.ndarray or None
            of type float, offset of each annotated segment in seconds
        labels : str, list, or numpy.ndarray
            of type str, label for each annotated segment

        Must specify both onsets and offsets,
        either in units of Hz or seconds (or both).
        """
        labels = cls._convert_labels(labels)

        (onsets_s, offsets_s, onset_samples, offset_samples, labels) = cls._validate_onsets_offsets_labels(
            onsets_s, offsets_s, onset_samples, offset_samples, labels
        )

        segments = []
        zipped = zip(labels, onset_samples, offset_samples, onsets_s, offsets_s)
        for label, onset_sample, offset_sample, onset_s, offset_s in zipped:
            segments.append(
                Segment(
                    label=label,
                    onset_sample=onset_sample,
                    offset_sample=offset_sample,
                    onset_s=onset_s,
                    offset_s=offset_s,
                )
            )

        return cls(segments, labels, onsets_s, offsets_s, onset_samples, offset_samples)

    @classmethod
    def from_dict(cls, seq_dict):
        """Construct a :class:`crowsetta.Sequence`
        from a :class:`dict` where keys
        are arguments to :meth:`~crowsetta.Sequence.from_keyword`.

        Parameters
        ----------
        seq_dict : dict
            with following key, value pairs
            onset_samples : numpy.ndarray or None
                of type int, onset of each annotated segment in samples/second
            offset_samples : numpy.ndarray or None
                of type int, offset of each annotated segment in samples/second
            onsets_s : numpy.ndarray or None
                of type float, onset of each annotated segment in seconds
            offsets_s : numpy.ndarray or None
                of type float, offset of each annotated segment in seconds
            labels : str, list, or numpy.ndarray
                of type str, label for each annotated segment

        ``seq_dict`` must specify both onsets and offsets,
        either in units of samples or seconds (or both).

        Examples
        --------
        >>> seq_dict = {
        ...     'labels': 'abc',
        ...     'onset_samples': np.asarray([16005, 17925, 19837]),
        ...     'offset_samples': np.asarray([17602, 19520, 21435]),
        ...     'file': 'bird0.wav',
        ...     }
        >>> seq = Sequence.from_dict(seq_dict)
        """
        # basically a convenience method
        # so user doesn't have to grok the concept of 'dictionary unpacking operator'
        return cls.from_keyword(**seq_dict)

    def as_dict(self) -> dict:
        """Convert this :class:`crowsetta.Sequence`
        to a :class:`dict`.

        Returns
        -------
        seq_dict : dict
            with the following key, value pairs:
                onset_samples : numpy.ndarray or None
                    of type int, onset of each annotated segment in samples/second
                offset_samples : numpy.ndarray or None
                    of type int, offset of each annotated segment in samples/second
                onsets_s : numpy.ndarray or None
                    of type float, onset of each annotated segment in seconds
                offsets_s : numpy.ndarray or None
                    of type float, offset of each annotated segment in seconds
                labels : numpy.ndarray
                    of type str; label for each annotated segment
        """
        seq_keys = ["onset_samples", "offset_samples", "onsets_s", "offsets_s", "labels"]
        seq_dict = dict(zip(seq_keys, [getattr(self, seq_key) for seq_key in seq_keys]))

        for a_key in ["onset_samples", "offset_samples", "onsets_s", "offsets_s"]:
            # if value is an array full of Nones, just convert to one None.
            # Use == to do elementwise comparison (so ignore warnings about
            # 'comparison with None performed with equality operators')
            if np.all(seq_dict[a_key] == None):  # noqa: E711
                seq_dict[a_key] = None

        return seq_dict
