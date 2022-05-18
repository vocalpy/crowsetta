import numpy as np
import pytest

import crowsetta.formats

from .asserts import assert_rounded_correct_num_decimals


def test_from_file(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    assert isinstance(textgrid, crowsetta.formats.seq.TextGrid)


def test_from_file_str(a_textgrid_path):
    a_textgrid_path_str = str(a_textgrid_path)
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path_str)
    assert isinstance(textgrid, crowsetta.formats.seq.TextGrid)


def test_to_seq(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq()
    assert isinstance(seq, crowsetta.Sequence)


@pytest.mark.parametrize(
    'decimals',
    [
        1,
        2,
        3,
        4,
        5,
    ]
)
def test_to_seq_round_times_true(test_data_root,
                                 a_textgrid_path,
                                 decimals):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root,
                                  a_textgrid_path):
    interval_tier = 0
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    seq = textgrid.to_seq(interval_tier=interval_tier, round_times=False)

    intv_tier = textgrid.textgrid[interval_tier]
    onsets_s = np.asarray(
        [interval.minTime for interval in intv_tier]
    )
    offsets_s = np.asarray(
        [interval.maxTime for interval in intv_tier]
    )

    assert np.all(
        np.allclose(seq.onsets_s, onsets_s)
    )
    assert np.all(
        np.allclose(seq.offsets_s, offsets_s)
    )


def test_to_annot(a_textgrid_path):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot()
    assert isinstance(annot, crowsetta.Annotation)
    assert hasattr(annot, 'seq')


@pytest.mark.parametrize(
    'decimals',
    [
        1,
        2,
        3,
        4,
        5,
    ]
)
def test_to_annot_round_times_true(test_data_root,
                                   a_textgrid_path,
                                   decimals):
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root,
                                    a_textgrid_path):
    interval_tier = 0
    textgrid = crowsetta.formats.seq.TextGrid.from_file(annot_path=a_textgrid_path)
    annot = textgrid.to_annot(interval_tier=interval_tier, round_times=False)

    intv_tier = textgrid.textgrid[interval_tier]
    onsets_s = np.asarray(
        [interval.minTime for interval in intv_tier]
    )
    offsets_s = np.asarray(
        [interval.maxTime for interval in intv_tier]
    )

    assert np.all(
        np.allclose(annot.seq.onsets_s, onsets_s)
    )
    assert np.all(
        np.allclose(annot.seq.offsets_s, offsets_s)
    )
