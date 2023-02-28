"""test functions in yarden module"""
import numpy as np
import pytest

import crowsetta

from .asserts import assert_rounded_correct_num_decimals


def test_from_file(yarden_annot_mat):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    assert isinstance(yarden, crowsetta.formats.seq.SongAnnotationGUI)


def test_from_file_str(yarden_annot_mat):
    yarden_annot_mat = str(yarden_annot_mat)
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    assert isinstance(yarden, crowsetta.formats.seq.SongAnnotationGUI)


def test_to_seq(yarden_annot_mat):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    seqs = yarden.to_seq()
    assert isinstance(seqs, list)
    assert all([isinstance(seq, crowsetta.Sequence) for seq in seqs])


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
def test_to_seq_round_times_true(test_data_root, yarden_annot_mat, decimals):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    seqs = yarden.to_seq(round_times=True, decimals=decimals)
    for seq in seqs:
        assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
        assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root, yarden_annot_mat):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    seq = yarden.to_seq(round_times=False)
    for seq, annotation in zip(seq, yarden.annotations):
        onsets_s = annotation["segFileStartTimes"].tolist()
        offsets_s = annotation["segFileEndTimes"].tolist()
        onsets_s = crowsetta.formats.seq.yarden._cast_to_arr(onsets_s)
        offsets_s = crowsetta.formats.seq.yarden._cast_to_arr(offsets_s)
        assert np.all(np.allclose(seq.onsets_s, onsets_s))
        assert np.all(np.allclose(seq.offsets_s, offsets_s))


def test_to_annot(yarden_annot_mat):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    annots = yarden.to_annot()
    assert isinstance(annots, list)
    assert all([isinstance(annot, crowsetta.Annotation) for annot in annots])


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
def test_to_annot_round_times_true(test_data_root, yarden_annot_mat, decimals):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    annots = yarden.to_annot(round_times=True, decimals=decimals)
    for annot in annots:
        assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
        assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root, yarden_annot_mat):
    yarden = crowsetta.formats.seq.SongAnnotationGUI.from_file(annot_path=yarden_annot_mat)
    annots = yarden.to_annot(round_times=False)

    for annot, annotation in zip(annots, yarden.annotations):
        onsets_s = annotation["segFileStartTimes"].tolist()
        offsets_s = annotation["segFileEndTimes"].tolist()
        onsets_s = crowsetta.formats.seq.yarden._cast_to_arr(onsets_s)
        offsets_s = crowsetta.formats.seq.yarden._cast_to_arr(offsets_s)
        assert np.all(np.allclose(annot.seq.onsets_s, onsets_s))
        assert np.all(np.allclose(annot.seq.offsets_s, offsets_s))
