import unittest

import numpy as np

from crowsetta.classes import Segment, SegmentList, Sequence


class TestSegmentList(unittest.TestCase):
    # test here because Sequence uses SegmentList
    def test_SegmentList_init(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        segments = SegmentList(segments=list_of_segments)
        self.assertTrue(type(segments) == SegmentList)
        self.assertTrue(hasattr(segments, 'segments'))

    def test_init_with_wrong_type_for_segments_raises(self):
        a_segment = Segment.from_keyword(
            label='a',
            onset_Hz=16000,
            offset_Hz=32000,
            file='bird21.wav'
        )
        list_of_segments = [a_segment] * 3
        set_of_segments = dict(zip(range(len(list_of_segments)),
                                   list_of_segments))
        with self.assertRaises(TypeError):
            SegmentList.from_list_or_tuple(segments=set_of_segments)

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
            SegmentList.from_list_or_tuple(segments=list_of_segments)


class TestSequence(unittest.TestCase):
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
        self.assertTrue(type(seq.segments) == SegmentList)

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
        self.assertTrue(type(seq.segments) == SegmentList)

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
        self.assertTrue(type(seq.segments) == SegmentList)

    def test_from_dict_onset_offset_in_seconds(self):
        annot_dict = {
            'file': '0.wav',
            'labels': 'abcde',
            'onsets_s':  np.asarray([0., 0.2, 0.4, 0.6, 0.8]),
            'offsets_s': np.asarray([0.1, 0.3, 0.5, 0.7, 0.9]),
        }
        seq = Sequence.from_dict(annot_dict=annot_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == SegmentList)

    def test_from_dict_onset_offset_in_Hertz(self):
        annot_dict = {
            'file': '0.wav',
            'labels': 'abcde',
            'onsets_Hz':  np.asarray([0, 2, 4, 6, 8]),
            'offsets_Hz': np.asarray([1, 3, 5, 7, 9]),
        }
        seq = Sequence.from_dict(annot_dict=annot_dict)
        self.assertTrue(hasattr(seq, 'segments'))
        self.assertTrue(type(seq.segments) == SegmentList)

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

if __name__ == '__main__':
    unittest.main()
