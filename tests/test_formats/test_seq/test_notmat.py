from pathlib import Path, PureWindowsPath

import numpy as np
import pytest

import crowsetta.formats

from .asserts import assert_rounded_correct_num_decimals


def test_load_notmat(a_notmat_path):
    notmat_dict = crowsetta.formats.seq.notmat.load_notmat(a_notmat_path)
    assert type(notmat_dict) is dict
    assert 'onsets' in notmat_dict
    assert type(notmat_dict['onsets']) == np.ndarray
    assert notmat_dict['onsets'].dtype == float
    assert 'offsets' in notmat_dict
    assert type(notmat_dict['offsets']) == np.ndarray
    assert notmat_dict['offsets'].dtype == float
    assert 'labels' in notmat_dict
    assert type(notmat_dict['labels']) == str
    assert 'Fs' in notmat_dict
    assert type(notmat_dict['Fs']) == int
    assert 'fname' in notmat_dict
    assert type(notmat_dict['fname']) == str
    assert 'min_int' in notmat_dict
    assert type(notmat_dict['min_int']) == int
    assert 'min_dur' in notmat_dict
    assert type(notmat_dict['min_dur']) == int
    assert 'threshold' in notmat_dict
    assert type(notmat_dict['threshold']) == int
    assert 'sm_win' in notmat_dict
    assert type(notmat_dict['sm_win']) == int


def test_load_notmat_single_annotated_segment(notmat_with_single_annotated_segment):
    notmat_dict = crowsetta.formats.seq.notmat.load_notmat(notmat_with_single_annotated_segment)
    assert type(notmat_dict) is dict
    assert 'onsets' in notmat_dict
    assert type(notmat_dict['onsets']) == np.ndarray
    assert notmat_dict['onsets'].dtype == float
    assert 'offsets' in notmat_dict
    assert type(notmat_dict['offsets']) == np.ndarray
    assert notmat_dict['offsets'].dtype == float
    assert 'labels' in notmat_dict
    assert type(notmat_dict['labels']) == str
    assert 'Fs' in notmat_dict
    assert type(notmat_dict['Fs']) == int
    assert 'fname' in notmat_dict
    assert type(notmat_dict['fname']) == str
    assert 'min_int' in notmat_dict
    assert type(notmat_dict['min_int']) == int
    assert 'min_dur' in notmat_dict
    assert type(notmat_dict['min_dur']) == int
    assert 'threshold' in notmat_dict
    assert type(notmat_dict['threshold']) == int
    assert 'sm_win' in notmat_dict
    assert type(notmat_dict['sm_win']) == int


def test_from_file(a_notmat_path):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    assert isinstance(notmat, crowsetta.formats.seq.NotMat)


def test_from_file_str(a_notmat_path):
    a_notmat_path_str = str(a_notmat_path)
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path_str)
    assert isinstance(notmat, crowsetta.formats.seq.NotMat)


def test_to_seq(a_notmat_path):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    seq = notmat.to_seq()
    assert isinstance(seq, crowsetta.Sequence)


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
def test_to_seq_round_times_true(test_data_root, a_notmat_path, decimals):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    seq = notmat.to_seq(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root, a_notmat_path):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    seq = notmat.to_seq(round_times=False)

    assert np.all(np.allclose(seq.onsets_s, notmat.onsets))
    assert np.all(np.allclose(seq.offsets_s, notmat.offsets))


def test_to_annot(a_notmat_path):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    annot = notmat.to_annot()
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
def test_to_annot_round_times_true(test_data_root, a_notmat_path, decimals):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    annot = notmat.to_annot(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root, a_notmat_path):
    notmat = crowsetta.formats.seq.NotMat.from_file(annot_path=a_notmat_path)
    annot = notmat.to_annot(round_times=False)

    assert np.all(np.allclose(annot.seq.onsets_s, notmat.onsets))
    assert np.all(np.allclose(annot.seq.offsets_s, notmat.offsets))


def test_to_file(tmp_path, a_notmat_path):
    notmat_dict = crowsetta.formats.seq.notmat.load_notmat(a_notmat_path)

    notmat = crowsetta.formats.seq.NotMat.from_file(a_notmat_path)
    notmat.to_file(
        samp_freq=notmat_dict["Fs"],
        threshold=notmat_dict["threshold"],
        min_syl_dur=notmat_dict["min_dur"] / 1000,
        min_silent_dur=notmat_dict["min_int"] / 1000,
        other_vars=None,
        dst=tmp_path,
    )
    notmat_made_path = tmp_path / (notmat.audio_path.name + ".not.mat")
    notmat_made = crowsetta.formats.seq.notmat.load_notmat(notmat_made_path)
    # can't do assert(new_dict == old_dict)
    # because headers will be different (and we want them to be different)
    for key in ["Fs", "fname", "labels", "onsets", "offsets", "min_int", "min_dur", "threshold", "sm_win"]:
        if key == "fname":
            # have to deal with Windows path saved in .not.mat files
            # and then compare file names without path to them
            notmat_dict_path = PureWindowsPath(notmat_dict[key])
            notmat_made_path = Path(notmat_made[key])
            assert notmat_dict_path.name == notmat_made_path.name
        elif type(notmat_dict[key]) == np.ndarray:
            assert np.allclose(notmat_dict[key], notmat_made[key], atol=1e-3, rtol=1e-3)
        else:
            assert notmat_dict[key] == notmat_made[key]
