import unittest

from crowsetta.segment import Segment


class TestSegment(unittest.TestCase):
    def test_Segment_init_onset_offset_in_seconds_from_keyword(self):
        a_segment = Segment.from_keyword(label='a',
                                         onset_s=0.123,
                                         offset_s=0.170)
        for attr in ['label', 'onset_s', 'offset_s']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_Hz', 'offset_Hz']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_onset_offset_in_Hertz_from_keyword(self):
        a_segment = Segment.from_keyword(label='a',
                                         onset_Hz=15655,
                                         offset_Hz=20001)
        for attr in ['label', 'onset_Hz', 'offset_Hz']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_s', 'offset_s']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_onset_offset_in_seconds_from_row(self):
        header = ['label', 'onset_s', 'offset_s', 'onset_Hz', 'offset_Hz']
        row = ['a', '0.123', '0.170', 'None', 'None']
        a_segment = Segment.from_row(row=row, header=header)
        for attr in ['label', 'onset_s', 'offset_s']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_Hz', 'offset_Hz']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_onset_offset_in_Hertz_from_row(self):
        header = ['label', 'onset_s', 'offset_s', 'onset_Hz', 'offset_Hz']
        row = ['a', 'None', 'None', '15655', '20001']
        a_segment = Segment.from_row(row=row, header=header)
        for attr in ['label', 'onset_Hz', 'offset_Hz']:
            self.assertTrue(hasattr(a_segment, attr))
        for attr in ['onset_s', 'offset_s']:
            self.assertTrue(getattr(a_segment, attr) is None)

    def test_Segment_init_missing_onsets_and_offsets_raises(self):
        with self.assertRaises(ValueError):
            a_segment = Segment.from_keyword(label='a')

    def test_Segment_init_missing_offset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = Segment.from_keyword(label='a',
                                             onset_s=0.123)

    def test_Segment_init_missing_onset_seconds_raises(self):
        with self.assertRaises(ValueError):
            a_segment = Segment.from_keyword(label='a',
                                             offset_s=0.177)

    def test_Segment_init_missing_offset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = Segment.from_keyword(label='a',
                                             onset_Hz=0.123)

    def test_Segment_init_missing_onset_Hertz_raises(self):
        with self.assertRaises(ValueError):
            a_segment = Segment.from_keyword(label='a',
                                             offset_Hz=0.177)


if __name__ == '__main__':
    unittest.main()
