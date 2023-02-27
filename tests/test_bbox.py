import pytest

import crowsetta


@pytest.mark.parametrize(
    "onset, offset, low_freq, high_freq, label",
    [
        (0.0, 1.0, 500.0, 12000.0, "a"),
        (0.0, 1.0, 500.0, 12000.0, "b"),
        (1.234, 3.595, 3000.0, 6600.0, "a"),
        (9.0, 12.653, 0.0, 20000.0, "z"),
        (22.123, 24.001, 1250.0, 9981.0, "@"),
        (22.123, 24.001, 1250.0, 9981.0, "@"),
    ],
)
def test_bbox(onset, offset, low_freq, high_freq, label):
    """smoke test that just tests whether we can create BBox instances"""
    bbox = crowsetta.BBox(onset=onset, offset=offset, low_freq=low_freq, high_freq=high_freq, label=label)
    assert isinstance(bbox, crowsetta.BBox)
    for attr_name, attr_val in zip(
        ("onset", "offset", "low_freq", "high_freq", "label"),
        (onset, offset, low_freq, high_freq, label),
    ):
        val_from_instance = getattr(bbox, attr_name)
        assert val_from_instance == attr_val


def test_onset_gt_offset_raises():
    with pytest.raises(ValueError):
        crowsetta.BBox(onset=1000.0, offset=0.0, low_freq=500.0, high_freq=12000.0, label="z")


def test_low_freq_gt_high_freq_raises():
    with pytest.raises(ValueError):
        crowsetta.BBox(onset=0.5, offset=1.5, low_freq=12000.0, high_freq=500.0, label="z")


@pytest.mark.parametrize(
    "onset, offset, low_freq, high_freq, label",
    [
        (0.0, -1.0, 500.0, 12000.0, "a"),
        (-1.234, 3.595, 3000.0, 6600.0, "a"),
        (22.123, 24.001, -1250.0, 9981.0, "@"),
        (9.0, 12.653, 0.0, -20000.0, "z"),
    ],
)
def test_neg_values_raise(onset, offset, low_freq, high_freq, label):
    """test that negative values raise an error"""
    with pytest.raises(ValueError):
        crowsetta.BBox(onset=onset, offset=offset, low_freq=low_freq, high_freq=high_freq, label=label)
