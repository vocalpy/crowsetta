import unittest

import crowsetta.classes


class Test_Classes(unittest.TestCase):
    def test_SegmentClass_init_onset_offset_in_seconds(self):
        a_segment = crowsetta.classes.SegmentClass(label='a',
                                                   onset_s=0.123,
                                                   offset_s=0.170,
                                                   file='bird21.wav')
        for attr in ['label', 'onset_s', 'offset_s', 'file']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_Hz', 'offset_Hz']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_SegmentClass_init_onset_offset_in_Hertz(self):
        a_segment = crowsetta.classes.SegmentClass(label='a',
                                                   onset_Hz=15655,
                                                   offset_Hz=20001,
                                                   file='bird21.wav')
        for attr in ['label', 'onset_Hz', 'offset_Hz', 'file']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_s', 'offset_s']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_SegmentClass_init_missing_onsets_and_offsets_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.SegmentClass(label='a',
                                                       file='bird21.wav')

    def test_SegmentClass_init_missing_offset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.SegmentClass(label='a',
                                                       onset_s=0.123,
                                                       file='bird21.wav')

    def test_SegmentClass_init_missing_onset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.SegmentClass(label='a',
                                                       offset_s=0.177,
                                                       file='bird21.wav')

    def test_SegmentClass_init_missing_offset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.SegmentClass(label='a',
                                                       onset_Hz=0.123,
                                                       file='bird21.wav')

    def test_SegmentClass_init_missing_onset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.SegmentClass(label='a',
                                                       offset_Hz=0.177,
                                                       file='bird21.wav')

    # -------------- test that everything holds true when we use Segment (class made with
    # -------------- attrs library) instead of SegmentClass

    def test_Segment_init_onset_offset_in_seconds(self):
        a_segment = crowsetta.classes.Segment(label='a',
                                              onset_s=0.123,
                                              offset_s=0.170,
                                              file='bird21.wav')
        for attr in ['label', 'onset_s', 'offset_s', 'file']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_Hz', 'offset_Hz']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_onset_offset_in_Hertz(self):
        a_segment = crowsetta.classes.Segment(label='a',
                                              onset_Hz=15655,
                                              offset_Hz=20001,
                                              file='bird21.wav')
        for attr in ['label', 'onset_Hz', 'offset_Hz', 'file']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_s', 'offset_s']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_missing_onsets_and_offsets_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.Segment(label='a',
                                                  file='bird21.wav')

    def test_Segment_init_missing_offset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.Segment(label='a',
                                                  onset_s=0.123,
                                                  file='bird21.wav')

    def test_Segment_init_missing_onset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.Segment(label='a',
                                                  offset_s=0.177,
                                                  file='bird21.wav')

    def test_Segment_init_missing_offset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.Segment(label='a',
                                                  onset_Hz=0.123,
                                                  file='bird21.wav')

    def test_Segment_init_missing_onset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = crowsetta.classes.Segment(label='a',
                                                  offset_Hz=0.177,
                                                  file='bird21.wav')

    def test_Sequence_init(self):
        a_sequence = crowsetta.classes.Sequence
        assert False


if __name__ == '__main__':
    unittest.main()
