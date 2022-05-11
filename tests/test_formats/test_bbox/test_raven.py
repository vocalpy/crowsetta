import filecmp

import pytest

import pandas as pd
import pandera

import crowsetta.formats


class TestRavenSchema:
    COLUMNS_MAP = {
        "Begin Time (s)": "begin_time_s",
        "End Time (s)": "end_time_s",
        "Low Freq (Hz)": "low_freq_hz",
        "High Freq (Hz)": "high_freq_hz",
        "Species": "annotation"
    }

    def test_raven_schema_phn_df(self,
                                 a_raven_txt_file):
        df = pd.read_csv(a_raven_txt_file, sep='\t')
        df.columns = df.columns.map(self.COLUMNS_MAP)
        df = crowsetta.formats.bbox.raven.RavenSchema.validate(df)
        # if validation worked, we get back a DataFrame
        assert isinstance(df, pd.DataFrame)

    def test_raven_schema_bad_df(self,
                                 a_raven_txt_file):
        df = pd.read_csv(a_raven_txt_file, sep='\t')
        # if we do not `map` the names, they will already be invalid
        with pytest.raises(pandera.errors.SchemaError):
            crowsetta.formats.bbox.raven.RavenSchema.validate(df)


def test_from_file(a_raven_txt_file,
                   raven_dataset_annot_col):
    raven = crowsetta.formats.bbox.Raven.from_file(annot_path=a_raven_txt_file,
                                                   annot_col=raven_dataset_annot_col)
    assert isinstance(raven, crowsetta.formats.bbox.Raven)


def test_from_file_str(a_raven_txt_file,
                       raven_dataset_annot_col):
    a_raven_txt_file = str(a_raven_txt_file)
    raven = crowsetta.formats.bbox.Raven.from_file(annot_path=a_raven_txt_file,
                                                   annot_col=raven_dataset_annot_col)
    assert isinstance(raven, crowsetta.formats.bbox.Raven)


def test_file_with_no_rows_raises(raven_txt_file_with_no_rows):
    with pytest.raises(ValueError):
        crowsetta.formats.bbox.Raven.from_file(annot_path=raven_txt_file_with_no_rows)


def test_to_bbox(a_raven_txt_file,
                 raven_dataset_annot_col):
    raven = crowsetta.formats.bbox.Raven.from_file(annot_path=a_raven_txt_file,
                                                   annot_col=raven_dataset_annot_col)
    bboxes = raven.to_bbox()
    assert isinstance(bboxes, list)
    assert all(
        [isinstance(bbox, crowsetta.BBox) for bbox in bboxes]
    )


def test_to_annot(a_raven_txt_file,
                  raven_dataset_annot_col):
    raven = crowsetta.formats.bbox.Raven.from_file(annot_path=a_raven_txt_file,
                                                   annot_col=raven_dataset_annot_col)
    annot = raven.to_annot()
    assert isinstance(annot, crowsetta.Annotation)
    assert hasattr(annot, 'bboxes')
    bboxes = annot.bboxes
    assert isinstance(bboxes, list)
    assert all(
        [isinstance(bbox, crowsetta.BBox) for bbox in bboxes]
    )


def test_to_raven(a_raven_txt_file,
                  raven_dataset_annot_col,
                  tmp_path):
    raven = crowsetta.formats.bbox.Raven.from_file(annot_path=a_raven_txt_file,
                                                   annot_col=raven_dataset_annot_col)
    annot_out_path = tmp_path / a_raven_txt_file.name
    raven.to_file(annot_path=annot_out_path)

    df_txt = pd.read_csv(a_raven_txt_file, sep='\t')
    df_out = pd.read_csv(annot_out_path, sep='\t')
    assert df_txt.equals(df_out)
