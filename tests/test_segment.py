import pytest

from crowsetta.segment import Segment


def test_Segment_init_onset_offset_in_seconds_from_keyword():
    a_segment = Segment.from_keyword(label='a',
                                     onset_s=0.123,
                                     offset_s=0.170)
    for attr in ['label', 'onset_s', 'offset_s']:
        assert hasattr(a_segment, attr)
    for attr in ['onset_Hz', 'offset_Hz']:
        assert getattr(a_segment, attr) is None


def test_Segment_init_onset_offset_in_Hertz_from_keyword():
    a_segment = Segment.from_keyword(label='a',
                                     onset_Hz=15655,
                                     offset_Hz=20001)
    for attr in ['label', 'onset_Hz', 'offset_Hz']:
        assert hasattr(a_segment, attr)
    for attr in ['onset_s', 'offset_s']:
        assert getattr(a_segment, attr) is None


def test_Segment_init_onset_offset_in_seconds_from_row():
    header = ['label', 'onset_s', 'offset_s', 'onset_Hz', 'offset_Hz']
    row = ['a', '0.123', '0.170', 'None', 'None']
    a_segment = Segment.from_row(row=row, header=header)
    for attr in ['label', 'onset_s', 'offset_s']:
        assert hasattr(a_segment, attr)
    for attr in ['onset_Hz', 'offset_Hz']:
        assert getattr(a_segment, attr) is None


def test_Segment_init_onset_offset_in_Hertz_from_row():
    header = ['label', 'onset_s', 'offset_s', 'onset_Hz', 'offset_Hz']
    row = ['a', 'None', 'None', '15655', '20001']
    a_segment = Segment.from_row(row=row, header=header)
    for attr in ['label', 'onset_Hz', 'offset_Hz']:
        assert hasattr(a_segment, attr)
    for attr in ['onset_s', 'offset_s']:
        assert getattr(a_segment, attr) is None


def test_Segment_init_missing_onsets_and_offsets_raises():
    with pytest.raises(ValueError):
        a_segment = Segment.from_keyword(label='a')


def test_Segment_init_missing_offset_seconds_raises():
    with pytest.raises(ValueError):
        a_segment = Segment.from_keyword(label='a',
                                         onset_s=0.123)


def test_Segment_init_missing_onset_seconds_raises():
    with pytest.raises(ValueError):
        a_segment = Segment.from_keyword(label='a',
                                         offset_s=0.177)


def test_Segment_init_missing_offset_Hertz_raises():
    with pytest.raises(ValueError):
        a_segment = Segment.from_keyword(label='a',
                                         onset_Hz=0.123)


def test_Segment_init_missing_onset_Hertz_raises():
    with pytest.raises(ValueError):
        a_segment = Segment.from_keyword(label='a',
                                         offset_Hz=0.177)
