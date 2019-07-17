import unittest

import numpy as np

from crowsetta.segment import Segment
from crowsetta.sequence import Sequence


class TestSequence(unittest.TestCase):

    @staticmethod
    def keywords_from_segments(segments):
        labels = []
        onsets_Hz = []
        offsets_Hz = []
        onsets_s = []
        offsets_s = []
        for seg in segments:
            labels.append(seg.label)
            onsets_Hz.append(seg.onset_Hz)
            offsets_Hz.append(seg.offset_Hz)
            onsets_s.append(None)
            offsets_s.append(None)
        onsets_Hz = np.asarray(onsets_Hz)
        offsets_Hz = np.asarray(offsets_Hz)
        onsets_s = np.asarray(onsets_s)
        offsets_s = np.asarray(offsets_s)
        return onsets_Hz, offsets_Hz, onsets_s, offsets_s, labels

    def setUp(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
        )
        list_of_segments = [a_segment] * 3

        (onsets_Hz,
         offsets_Hz,
         onsets_s,
         offsets_s,
         labels) = self.keywords_from_segments(list_of_segments)

        self.a_seq = Sequence(segments=list_of_segments,
                              onsets_Hz=onsets_Hz,
                              offsets_Hz=offsets_Hz,
                              onsets_s=onsets_s,
                              offsets_s=offsets_s,
                              labels=labels,
                              )

        self.same_seq = Sequence(segments=list_of_segments,
                                 onsets_Hz=onsets_Hz,
                                 offsets_Hz=offsets_Hz,
                                 onsets_s=onsets_s,
                                 offsets_s=offsets_s,
                                 labels=labels,
                                 )

        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=32000,
            offset_Hz=64000,
        )
        list_of_segments = [a_segment] * 4

        (onsets_Hz,
         offsets_Hz,
         onsets_s,
         offsets_s,
         labels) = self.keywords_from_segments(list_of_segments)

        self.different_seq = Sequence(segments=list_of_segments,
                                      onsets_Hz=onsets_Hz,
                                      offsets_Hz=offsets_Hz,
                                      onsets_s=onsets_s,
                                      offsets_s=offsets_s,
                                      labels=labels,
                                      )

    def test_init(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
        )
        list_of_segments = [a_segment] * 3

        (onsets_Hz,
         offsets_Hz,
         onsets_s,
         offsets_s,
         labels) = self.keywords_from_segments(list_of_segments)

        seq = Sequence(segments=list_of_segments,
                       onsets_Hz=onsets_Hz,
                       offsets_Hz=offsets_Hz,
                       onsets_s=onsets_s,
                       offsets_s=offsets_s,
                       labels=labels,
                       )

        self.assertTrue(type(seq) == Sequence)
        self.assertTrue(hasattr(seq, 'segments'))

    def test_init_with_wrong_type_for_segments_raises(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
        )
        list_of_segments = [a_segment] * 3
        dict_of_segments = dict(zip(range(len(list_of_segments)),
                                    list_of_segments))
        with self.assertRaises(TypeError):
            Sequence(segments=dict_of_segments)

    def test_init_with_bad_type_in_segments_raises(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
        )
        list_of_segments = [a_segment] * 3
        segment_dict = {
            'label': 'a',
            'onset_Hz': 16000,
            'offset_Hz': 32000,
        }
        list_of_segments.append(segment_dict)
        with self.assertRaises(TypeError):
            Sequence(segments=list_of_segments)

    def test_from_segments(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
        )
        list_of_segments = [a_segment] * 3
        seq = Sequence.from_segments(list_of_segments)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == tuple)

    def test_from_keyword_bad_labels_type_raises(self):
        labels = 12345
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        with self.assertRaises(TypeError):
            Sequence.from_keyword(labels=labels, onsets_Hz=onsets_Hz,
                                  offsets_Hz=offsets_Hz)

    def test_from_keyword__onset_offset_in_seconds(self):
        labels = 'abcde'
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8])
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == tuple)

    def test_from_keyword_onset_offset_in_Hertz(self):
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == tuple)

    def test_from_dict_onset_offset_in_seconds(self):
        seq_dict = {
            'labels': 'abcde',
            'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
            'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        }
        seq = Sequence.from_dict(seq_dict=seq_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == tuple)

    def test_from_dict_onset_offset_in_Hertz(self):
        seq_dict = {
            'labels': 'abcde',
            'onsets_Hz':  np.asarray([0, 2, 4, 6, 8]),
            'offsets_Hz': np.asarray([1, 3, 5, 7, 9]),
        }
        seq = Sequence.from_dict(seq_dict=seq_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == tuple)

    def test_from_keyword_missing_onsets_and_offsets_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde')

    def test_missing_offset_seconds_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  onsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]))

    def test_missing_onset_seconds_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  offsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]))

    def test_missing_offset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  onsets_Hz=np.asarray([0, 2, 4, 6, 8]))

    def test_missing_onset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  offsets_Hz=np.asarray([0, 2, 4, 6, 8]))

    def test_as_dict_onset_offset_in_Hertz(self):
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz)
        seq_dict = seq.as_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_Hz'] == onsets_Hz))
        self.assertTrue(np.all(seq_dict['offsets_Hz'] == offsets_Hz))
        self.assertTrue(seq_dict['onsets_s'] is None)
        self.assertTrue(seq_dict['offsets_s'] is None)

    def test_as_dict_onset_offset_in_seconds(self):
        labels = 'abcde'
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s)
        seq_dict = seq.as_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_s'] == onsets_s))
        self.assertTrue(np.all(seq_dict['offsets_s'] == offsets_s))
        self.assertTrue(seq_dict['onsets_Hz'] is None)
        self.assertTrue(seq_dict['offsets_Hz'] is None)

    def test_to_dict_onset_offset_both_units(self):
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s)
        seq_dict = seq.as_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_s'] == onsets_s))
        self.assertTrue(np.all(seq_dict['offsets_s'] == offsets_s))
        self.assertTrue(np.all(seq_dict['onsets_Hz'] == onsets_Hz))
        self.assertTrue(np.all(seq_dict['offsets_Hz'] == offsets_Hz))

    def test_eq(self):
        self.assertTrue(self.a_seq == self.same_seq)

    def test_ne(self):
        self.assertTrue(self.a_seq != self.different_seq)

    def test_lt_raises(self):
        with self.assertRaises(NotImplementedError):
            self.a_seq < self.different_seq

    def test_le_raises(self):
        with self.assertRaises(NotImplementedError):
            self.a_seq <= self.different_seq

    def test_gt_raises(self):
        with self.assertRaises(NotImplementedError):
            self.a_seq > self.different_seq

    def test_ge_raises(self):
        with self.assertRaises(NotImplementedError):
            self.a_seq >= self.different_seq

    def test_hash(self):
        seq_dict1 = {
            'labels': 'abcde',
            'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
            'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        }
        seq1 = Sequence.from_dict(seq_dict=seq_dict1)

        # same as seq1, so Sequence should have same hash
        seq_dict2 = {
            'labels': 'abcde',
            'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
            'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        }
        seq2 = Sequence.from_dict(seq_dict=seq_dict2)

        # different from seq1, so Sequence should have different hash
        seq_dict3 = {'labels': 'fghijk',
                     'onsets_s': np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
                     'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
                     }
        seq3 = Sequence.from_dict(seq_dict=seq_dict3)

        hash1 = hash(seq1)
        hash2 = hash(seq2)
        hash3 = hash(seq3)

        self.assertTrue(hash1 == hash2)
        self.assertTrue(hash1 != hash3)

    def test_seq_is_immutable(self):
        with self.assertRaises(TypeError):
            self.a_seq.labels = np.asarray(['a', 'b', 'c', 'd', 'd'])


if __name__ == '__main__':
    unittest.main()
