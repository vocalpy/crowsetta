import filecmp

import pandas as pd
import pandera
import pytest

import crowsetta.formats


class TestTimitTranscriptSchema:
    def test_timit_schema_phn_df(self, a_transcript_path):
        phn_df = pd.read_csv(a_transcript_path, sep=" ", header=None)
        phn_df.columns = ["begin_sample", "end_sample", "text"]
        phn_df = crowsetta.formats.seq.timit.TimitTranscriptSchema.validate(phn_df)
        # if validation worked, we get back a DataFrame
        assert isinstance(phn_df, pd.DataFrame)

    def test_timit_schema_bad_df(self, a_transcript_path):
        phn_df = pd.read_csv(a_transcript_path, sep=" ", header=None)
        # notice: wrong column names
        phn_df.columns = ["text", "begin_sample", "end_sample"]
        with pytest.raises(pandera.errors.SchemaError):
            phn_df = crowsetta.formats.seq.timit.TimitTranscriptSchema.validate(phn_df)


def test_from_file(a_transcript_path):
    phn = crowsetta.formats.seq.Timit.from_file(annot_path=a_transcript_path)
    assert isinstance(phn, crowsetta.formats.seq.Timit)


def test_from_file_str(a_transcript_path):
    a_transcript_path = str(a_transcript_path)
    phn = crowsetta.formats.seq.Timit.from_file(annot_path=a_transcript_path)
    assert isinstance(phn, crowsetta.formats.seq.Timit)


def test_to_seq(a_transcript_path):
    phn = crowsetta.formats.seq.Timit.from_file(annot_path=a_transcript_path)
    seq = phn.to_seq()
    assert isinstance(seq, crowsetta.Sequence)


def test_to_annot(a_transcript_path):
    phn = crowsetta.formats.seq.Timit.from_file(annot_path=a_transcript_path)
    annot = phn.to_annot()
    assert isinstance(annot, crowsetta.Annotation)


def test_to_timit(a_transcript_path, tmp_path):
    phn = crowsetta.formats.seq.Timit.from_file(annot_path=a_transcript_path)
    annot_path = tmp_path / a_transcript_path.name
    phn.to_file(annot_path=annot_path)
    assert filecmp.cmp(a_transcript_path, annot_path)
