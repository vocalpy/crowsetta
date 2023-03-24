import numpy as np
import pytest

import crowsetta.formats
from crowsetta.formats.seq.textgrid.classes import IntervalTier

from ..asserts import assert_rounded_correct_num_decimals


def test_from_file(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    assert isinstance(textgrid, crowsetta.formats.seq.TextGrid)


def test_from_file_str(a_textgrid_path):
    a_textgrid_path_str = str(a_textgrid_path)
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path_str)
    assert isinstance(textgrid, crowsetta.formats.seq.TextGrid)


def test_from_file_keep_empty(a_textgrid_with_empty_intervals_path, keep_empty):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_with_empty_intervals_path,
                                                        keep_empty=keep_empty)
    tiers = [tier for tier in textgrid.tiers if isinstance(tier, IntervalTier)]

    if keep_empty:
        assert any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )
    else:
        assert not any(
            [interval.text == ""
             for tier in tiers
             for interval in tier]
        )


def test_to_seq(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq()
    assert isinstance(seq, (crowsetta.Sequence, list))
    if isinstance(seq, list):
        assert all([isinstance(seq_, crowsetta.Sequence) for seq_ in seq])


@pytest.mark.parametrize(
    "decimals",
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
def test_to_seq_round_times_true(a_textgrid_path, decimals):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq(round_times=True, decimals=decimals)

    if isinstance(seq, crowsetta.Sequence):
        assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
        assert_rounded_correct_num_decimals(seq.offsets_s, decimals)
    elif isinstance(seq, list):
        for seq_ in seq:
            assert_rounded_correct_num_decimals(seq_.onsets_s, decimals)
            assert_rounded_correct_num_decimals(seq_.offsets_s, decimals)


def test_to_seq_round_times_false(a_textgrid_path):
    tier = 0
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq(tier=tier, round_times=False)

    intv_tier = textgrid[tier]
    onsets_s = np.asarray([interval.xmin for interval in intv_tier])
    offsets_s = np.asarray([interval.xmax for interval in intv_tier])

    if isinstance(seq, crowsetta.Sequence):
        assert np.all(np.allclose(seq.onsets_s, onsets_s))
        assert np.all(np.allclose(seq.offsets_s, offsets_s))
    elif isinstance(seq, list):
        breakpoint()
        for seq_ in seq:
            assert np.all(np.allclose(seq_.onsets_s, onsets_s))
            assert np.all(np.allclose(seq_.offsets_s, offsets_s))


def test_to_annot(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot()
    assert isinstance(annot, crowsetta.Annotation)
    assert hasattr(annot, "seq")


@pytest.mark.parametrize(
    "decimals",
    [
        1,
        2,
        3,
        4,
        5,
    ],
)
def test_to_annot_round_times_true(a_textgrid_path, decimals):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot(round_times=True, decimals=decimals)
    if isinstance(annot.seq, crowsetta.Sequence):
        assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
        assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)
    elif isinstance(annot.seq, list):
        for seq_ in annot.seq:
            assert_rounded_correct_num_decimals(seq_.onsets_s, decimals)
            assert_rounded_correct_num_decimals(seq_.offsets_s, decimals)


def test_to_annot_round_times_false(a_textgrid_path):
    tier = 0
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot(tier=tier, round_times=False)

    intv_tier = textgrid[tier]
    onsets_s = np.asarray([interval.xmin for interval in intv_tier])
    offsets_s = np.asarray([interval.xmax for interval in intv_tier])

    assert np.all(np.allclose(annot.seq.onsets_s, onsets_s))
    assert np.all(np.allclose(annot.seq.offsets_s, offsets_s))
