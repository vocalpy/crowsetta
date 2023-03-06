import pytest

from crowsetta.segment import Segment

@pytest.mark.parametrize(
    'kwargs',
    [
        dict(label="a", onset_s=0.123, offset_s=0.170),
        dict(label="a", onset_sample=15655, offset_sample=20001),

    ]
)
def test_Segment(kwargs):
    a_segment = Segment(**kwargs)
    for attr in ["label", "onset_s", "offset_s", "onset_sample", "offset_sample"]:
        if attr in kwargs:
            assert hasattr(a_segment, attr)
            assert getattr(a_segment, attr) == kwargs[attr]
        else:
            assert getattr(a_segment, attr) is None


@pytest.mark.parametrize(
    'kwargs, expected_error',
    [
        (dict(label="a",), ValueError),
        (dict(label="a", onset_s=0.123), ValueError),
        (dict(label="a", offset_s=0.177), ValueError),
        (dict(label="a", onset_sample=15655), ValueError),
        (dict(label="a", offset_sample=20001), ValueError),
        (dict(label="a", onset_s=15655), TypeError),
        (dict(label="a", offset_s=20001), TypeError),
        (dict(label="a", onset_sample=0.123), TypeError),
        (dict(label="a", offset_sample=0.177), TypeError),
    ]
)
def test_Segment_raises(kwargs, expected_error):
    with pytest.raises(expected_error):
        Segment(**kwargs)
