import filecmp

import numpy as np
import pytest

import pandas as pd
import pandera

import crowsetta.formats

from .asserts import assert_rounded_correct_num_decimals


class TestAudTxtSchema:
    def test_audtxt_schema(self,
                           an_audtxt_path):
        audtxt_df = pd.read_csv(an_audtxt_path, sep='\t', header=None)
        audtxt_df.columns = ['start_time', 'end_time', 'label']
        simple_df = crowsetta.formats.seq.audtxt.AudTxtSchema.validate(audtxt_df)
        # if validation worked, we get back a DataFrame
        assert isinstance(simple_df, pd.DataFrame)

    def test_audtxt_schema_bad_df(self,
                                  an_audtxt_path):
        audtxt_df = pd.read_csv(an_audtxt_path, sep='\t', header=None)
        # notice: wrong column name 'stop_time'
        audtxt_df.columns = ['start_time', 'stop_time', 'label']
        with pytest.raises(pandera.errors.SchemaError):
            crowsetta.formats.seq.audtxt.AudTxtSchema.validate(audtxt_df)


def test_from_file(an_audtxt_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    assert isinstance(audtxt, crowsetta.formats.seq.AudTxt)


def test_from_file_str(an_audtxt_path):
    an_audtxt_path = str(an_audtxt_path)
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    assert isinstance(audtxt, crowsetta.formats.seq.AudTxt)


def test_to_seq(an_audtxt_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    seq = audtxt.to_seq()
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
                                 an_audtxt_path,
                                 decimals):
    simple = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    seq = simple.to_seq(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(seq.offsets_s, decimals)


def test_to_seq_round_times_false(test_data_root,
                                  an_audtxt_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    seq = audtxt.to_seq(round_times=False)

    assert np.all(
        np.allclose(seq.onsets_s, audtxt.start_times)
    )
    assert np.all(
        np.allclose(seq.offsets_s, audtxt.end_times)
    )


def test_to_annot(an_audtxt_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    annot = audtxt.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


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
                                   an_audtxt_path,
                                   decimals):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    annot = audtxt.to_annot(round_times=True, decimals=decimals)
    assert_rounded_correct_num_decimals(annot.seq.onsets_s, decimals)
    assert_rounded_correct_num_decimals(annot.seq.offsets_s, decimals)


def test_to_annot_round_times_false(test_data_root,
                                    an_audtxt_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    annot = audtxt.to_annot(round_times=False)

    assert np.all(
        np.allclose(annot.seq.onsets_s, audtxt.start_times)
    )
    assert np.all(
        np.allclose(annot.seq.offsets_s, audtxt.end_times)
    )


def test_to_file(an_audtxt_path,
                 tmp_path):
    audtxt = crowsetta.formats.seq.AudTxt.from_file(annot_path=an_audtxt_path)
    csv_path = tmp_path / an_audtxt_path.name
    audtxt.to_file(annot_path=csv_path)
    assert filecmp.cmp(an_audtxt_path, csv_path)
