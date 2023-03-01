import filecmp

import numpy as np
import pandas as pd
import pandera
import pytest

import crowsetta.formats

from .asserts import assert_rounded_correct_num_decimals


class TestAudSeqSchema:
    def test_audseq_schema(self, an_audseq_path):
        audseq_df = pd.read_csv(an_audseq_path, sep="\t", header=None)
        audseq_df.columns = ["start_time", "end_time", "label"]
        simple_df = crowsetta.formats.seq.audseq.AudSeqSchema.validate(audseq_df)
        # if validation worked, we get back a DataFrame
        assert isinstance(simple_df, pd.DataFrame)

    def test_audseq_schema_bad_df(self, an_audseq_path):
        audseq_df = pd.read_csv(an_audseq_path, sep="\t", header=None)
        # notice: wrong column name 'stop_time'
        audseq_df.columns = ["start_time", "stop_time", "label"]
        with pytest.raises(pandera.errors.SchemaError):
            crowsetta.formats.seq.audseq.AudSeqSchema.validate(audseq_df)


def test_from_file(an_audseq_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    assert isinstance(audseq, crowsetta.formats.seq.AudSeq)


def test_from_file_str(an_audseq_path):
    an_audseq_path = str(an_audseq_path)
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    assert isinstance(audseq, crowsetta.formats.seq.AudSeq)


def test_to_seq(an_audseq_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    seq = audseq.to_seq()
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
def test_to_seq_round_times_true(test_data_root, an_audseq_path, decimals):
    simple = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    seq = simple.to_seq(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root, an_audseq_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    seq = audseq.to_seq(round_times=False)

    assert np.all(np.allclose(seq.onsets_s, audseq.start_times))
    assert np.all(np.allclose(seq.offsets_s, audseq.end_times))


def test_to_annot(an_audseq_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    annot = audseq.to_annot()
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
def test_to_annot_round_times_true(test_data_root, an_audseq_path, decimals):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    annot = audseq.to_annot(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root, an_audseq_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    annot = audseq.to_annot(round_times=False)

    assert np.all(np.allclose(annot.seq.onsets_s, audseq.start_times))
    assert np.all(np.allclose(annot.seq.offsets_s, audseq.end_times))


def test_to_file(an_audseq_path, tmp_path):
    audseq = crowsetta.formats.seq.AudSeq.from_file(annot_path=an_audseq_path)
    csv_path = tmp_path / an_audseq_path.name
    audseq.to_file(annot_path=csv_path)
    assert filecmp.cmp(an_audseq_path, csv_path)
