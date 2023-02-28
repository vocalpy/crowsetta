import pandas as pd
import pandera
import pytest

import crowsetta.formats


def test_txt_to_records(an_audbbox_path):
    records = crowsetta.formats.bbox.audbbox.txt_to_records(an_audbbox_path)
    assert isinstance(records, list)
    assert all(
        [isinstance(record, dict) for record in records]
    )
    assert all(
        [
            all([key in record
                 for key in ('begin_time_s', 'end_time_s', 'label', 'low_freq_hz', 'high_freq_hz',)])
            for record in records
        ]
    )
    with an_audbbox_path.open('r') as fp:
        lines = fp.read().splitlines()
    assert len(records) == len(lines) / 2


def test_df_to_lines(an_audbbox_path, tmp_path):
    # ---- test set-up
    # we test by round-trip; df_to_audbbox_txt should be the inverse of:
    # (1) audbbox_txt_to_df + (2) validation with schema
    records = crowsetta.formats.bbox.audbbox.txt_to_records(an_audbbox_path)
    df = pd.DataFrame.from_records(records)
    df = crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(df)

    lines = crowsetta.formats.bbox.audbbox.df_to_lines(df)
    test_txt_path = tmp_path / 'test.txt'
    with test_txt_path.open('w') as fp:
        fp.writelines(lines)

    records_test = crowsetta.formats.bbox.audbbox.txt_to_records(test_txt_path)
    # test that we can round-trip and get the same answer
    assert records_test == records


class TestAudBBoxSchema:
    def test_aud_bbox_schema_df(self, an_audbbox_path):
        records = crowsetta.formats.bbox.audbbox.txt_to_records(an_audbbox_path)
        df = pd.DataFrame.from_records(records)
        df = crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(df)
        # if validation worked, we get back a DataFrame
        assert isinstance(df, pd.DataFrame)

    def test_raven_schema_bad_df(self, an_audbbox_path):
        # if we just load the csv directly, it will be invalid
        df = pd.read_csv(an_audbbox_path, sep="\t", header=None)

        with pytest.raises(pandera.errors.SchemaError):
            crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(df)


def test_from_file(an_audbbox_path):
    audbbox = crowsetta.formats.bbox.AudBBox.from_file(annot_path=an_audbbox_path)
    assert isinstance(audbbox, crowsetta.formats.bbox.AudBBox)


def test_from_file_str(an_audbbox_path):
    an_audbbox_path = str(an_audbbox_path)
    audbbox = crowsetta.formats.bbox.AudBBox.from_file(annot_path=an_audbbox_path)
    assert isinstance(audbbox, crowsetta.formats.bbox.AudBBox)


def test_file_with_no_rows_raises(raven_txt_file_with_no_rows):
    # recycle same fixture we use with Raven, it's still just a .txt file with no rows
    with pytest.raises(ValueError):
        crowsetta.formats.bbox.AudBBox.from_file(annot_path=raven_txt_file_with_no_rows)


def test_to_bbox(an_audbbox_path, raven_dataset_annot_col):
    audbbox = crowsetta.formats.bbox.AudBBox.from_file(annot_path=an_audbbox_path)
    bboxes = audbbox.to_bbox()
    assert isinstance(bboxes, list)
    assert all([isinstance(bbox, crowsetta.BBox) for bbox in bboxes])


def test_to_annot(an_audbbox_path, raven_dataset_annot_col):
    audbbox = crowsetta.formats.bbox.AudBBox.from_file(annot_path=an_audbbox_path)
    annot = audbbox.to_annot()
    assert isinstance(annot, crowsetta.Annotation)
    assert hasattr(annot, "bboxes")
    bboxes = annot.bboxes
    assert isinstance(bboxes, list)
    assert all([isinstance(bbox, crowsetta.BBox) for bbox in bboxes])


def test_to_file(an_audbbox_path, tmp_path):
    audbbox = crowsetta.formats.bbox.AudBBox.from_file(annot_path=an_audbbox_path)
    annot_out_path = tmp_path / an_audbbox_path.name
    audbbox.to_file(annot_path=annot_out_path)

    records = crowsetta.formats.bbox.audbbox.txt_to_records(an_audbbox_path)
    expected_df = pd.DataFrame.from_records(records)
    expected_df = crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(expected_df)

    records_txt = crowsetta.formats.bbox.audbbox.txt_to_records(annot_out_path)
    txt_df = pd.DataFrame.from_records(records_txt)
    txt_df = crowsetta.formats.bbox.audbbox.AudBBoxSchema.validate(txt_df)

    pd.testing.assert_frame_equal(txt_df, expected_df)
