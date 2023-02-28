import filecmp

import numpy as np
import pandas as pd
import pandera
import pytest

import crowsetta.formats

from .asserts import assert_rounded_correct_num_decimals


class TestSimpleSeqSchema:
    def test_simple_seq_schema_phn_df(self, a_simple_csv_path):
        simple_df = pd.read_csv(a_simple_csv_path)
        simple_df = crowsetta.formats.seq.simple.SimpleSeqSchema.validate(simple_df)
        # if validation worked, we get back a DataFrame
        assert isinstance(simple_df, pd.DataFrame)

    def test_simple_seq_schema_bad_df(self, a_simple_csv_path):
        simple_df = pd.read_csv(a_simple_csv_path)
        # notice: wrong column names
        simple_df.columns = ["text", "begin_sample", "end_sample"]
        with pytest.raises(pandera.errors.SchemaError):
            simple_df = crowsetta.formats.seq.simple.SimpleSeqSchema.validate(simple_df)


def test_from_file(a_simple_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)


def test_from_file_str(a_simple_csv_path):
    a_simple_csv_path = str(a_simple_csv_path)
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)


def test_from_file_das(a_das_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(
        annot_path=a_das_csv_path,
        read_csv_kwargs={"index_col": 0},
        columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s", "name": "label"},
    )
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)


def test_to_seq(a_simple_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    seq = simple.to_seq()
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
def test_to_seq_round_times_true(test_data_root, a_simple_csv_path, decimals):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    seq = simple.to_seq(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root, a_simple_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    seq = simple.to_seq(round_times=False)

    assert np.all(np.allclose(seq.onsets_s, simple.onsets_s))
    assert np.all(np.allclose(seq.offsets_s, simple.offsets_s))


def test_to_annot(a_simple_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    annot = simple.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


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
def test_to_annot_round_times_true(test_data_root, a_simple_csv_path, decimals):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    annot = simple.to_annot(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root, a_simple_csv_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    annot = simple.to_annot(round_times=False)

    assert np.all(np.allclose(annot.seq.onsets_s, simple.onsets_s))
    assert np.all(np.allclose(annot.seq.offsets_s, simple.offsets_s))


def test_to_file(a_simple_csv_path, tmp_path):
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=a_simple_csv_path)
    csv_path = tmp_path / a_simple_csv_path.name
    simple.to_file(annot_path=csv_path)
    assert filecmp.cmp(a_simple_csv_path, csv_path)
