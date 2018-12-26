import unittest

import numpy as np

from crowsetta.classes import Segment, Sequence


class TestSequence(unittest.TestCase):
    # test here because Sequence uses SegmentList
    def test_init(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        seq = Sequence(segments=list_of_segments)
        self.assertTrue(type(seq) == Sequence)
        self.assertTrue(hasattr(seq, 'segments'))

    def test_init_with_wrong_type_for_segments_raises(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
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
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        segment_dict = {
            'label': 'a',
            'onset_Hz': 16000,
            'offset_Hz': 32000,
            'file': 'bird21.wav',
        }
        list_of_segments.append(segment_dict)
        with self.assertRaises(TypeError):
            Sequence(segments=list_of_segments)

    def test_from_segments(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        seq = Sequence.from_segments(list_of_segments)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == list)

    def test_from_keyword_bad_labels_type_raises(self):
        file = '0.wav'
        labels = 12345
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        with self.assertRaises(TypeError):
            Sequence.from_keyword(file=file, labels=labels, 
                                  onsets_Hz=onsets_Hz, offsets_Hz=offsets_Hz)

    def test_from_keyword__onset_offset_in_seconds(self):
        file = '0.wav'
        labels = 'abcde'
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8])
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s,
                                    file=file)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == list)

    def test_from_keyword_onset_offset_in_Hertz(self):
        file = '0.wav'
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz,
                                    file=file)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == list)

    def test_from_dict_onset_offset_in_seconds(self):
        annot_dict = {
            'file': '0.wav',
            'labels': 'abcde',
            'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
            'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        }
        seq = Sequence.from_dict(annot_dict=annot_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == list)

    def test_from_dict_onset_offset_in_Hertz(self):
        annot_dict = {
            'file': '0.wav',
            'labels': 'abcde',
            'onsets_Hz':  np.asarray([0, 2, 4, 6, 8]),
            'offsets_Hz': np.asarray([1, 3, 5, 7, 9]),
        }
        seq = Sequence.from_dict(annot_dict=annot_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == list)

    def test_from_keyword_missing_onsets_and_offsets_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  file='bird21.wav')

    def test_missing_offset_seconds_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  onsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
                                  file='bird21.wav')

    def test_missing_onset_seconds_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  offsets_s=np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
                                  file='bird21.wav')

    def test_missing_offset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  onsets_Hz=np.asarray([0, 2, 4, 6, 8]),
                                  file='bird21.wav')

    def test_missing_onset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            Sequence.from_keyword(labels='abcde',
                                  offsets_Hz=np.asarray([0, 2, 4, 6, 8]),
                                  file='bird21.wav')

    def test_to_dict_onset_offset_in_Hertz(self):
        file = '0.wav'
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz,
                                    file=file)
        seq_dict = seq.to_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_Hz'] == onsets_Hz))
        self.assertTrue(np.all(seq_dict['offsets_Hz'] == offsets_Hz))
        self.assertTrue(np.all(seq_dict['file'] == file))
        self.assertTrue(seq_dict['onsets_s'] is None)
        self.assertTrue(seq_dict['offsets_s'] is None)

    def test_to_dict_onset_offset_in_seconds(self):
        file = '0.wav'
        labels = 'abcde'
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s,
                                    file=file)
        seq_dict = seq.to_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_s'] == onsets_s))
        self.assertTrue(np.all(seq_dict['offsets_s'] == offsets_s))
        self.assertTrue(np.all(seq_dict['file'] == file))
        self.assertTrue(seq_dict['onsets_Hz'] is None)
        self.assertTrue(seq_dict['offsets_Hz'] is None)

    def test_to_dict_onset_offset_both_units(self):
        file = '0.wav'
        labels = 'abcde'
        onsets_Hz = np.asarray([0, 2, 4, 6, 8])
        offsets_Hz = np.asarray([1, 3, 5, 7, 9])
        onsets_s = np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
        offsets_s = np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        seq = Sequence.from_keyword(labels=labels,
                                    onsets_Hz=onsets_Hz,
                                    offsets_Hz=offsets_Hz,
                                    onsets_s=onsets_s,
                                    offsets_s=offsets_s,
                                    file=file)
        seq_dict = seq.to_dict()

        self.assertTrue(np.all(seq_dict['labels'] == np.asarray(list(labels))))
        self.assertTrue(np.all(seq_dict['onsets_s'] == onsets_s))
        self.assertTrue(np.all(seq_dict['offsets_s'] == offsets_s))
        self.assertTrue(np.all(seq_dict['onsets_Hz'] == onsets_Hz))
        self.assertTrue(np.all(seq_dict['offsets_Hz'] == offsets_Hz))
        self.assertTrue(np.all(seq_dict['file'] == file))

    def test_to_dict_with_bad_Segments_raises(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        segment_with_different_file = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird12.wav'
        )
        list_of_segments.append(segment_with_different_file)
        seq = Sequence(segments=list_of_segments)
        with self.assertRaises(ValueError):
            seq.to_dict()


if __name__ == '__main__':
    unittest.main()
