import filecmp
import inspect
import tempfile

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


@pytest.fixture
def empty_csv_file_path(tmpdir):
    empty_df = pd.DataFrame.from_records([])
    empty_csv_file_path = tmpdir / "empty.csv"
    empty_df.to_csv(empty_csv_file_path)
    return empty_csv_file_path


def test_empty_annotations(empty_csv_file_path):
    # test fix for https://github.com/vocalpy/crowsetta/issues/264
    simple = crowsetta.formats.seq.SimpleSeq.from_file(annot_path=empty_csv_file_path)
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)
    for attr in ("onsets_s", "offsets_s", "labels"):
        assert np.array_equal(
            getattr(simple, attr), np.array([])
        )
    seq = simple.to_seq()
    assert len(seq) == 0


def test_columns_map_only_maps_columns(jourjine_et_al_2023_csv_path):
    # test fixes for https://github.com/vocalpy/crowsetta/issues/272
    simple = crowsetta.formats.seq.SimpleSeq.from_file(
        annot_path=jourjine_et_al_2023_csv_path,
        columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s"}
    )
    assert isinstance(simple, crowsetta.formats.seq.SimpleSeq)


@pytest.mark.parametrize(
        'columns_map, expected_exception',
        [
            # not a dict, throws a TypeError
            ([], TypeError),
            # not all key-value pairs are string to string
            ({"start_seconds": "onset_s", "stop_seconds": 0}, ValueError),
            # invalid value, not in ("onset_s", "offset_s", "label")
            ({"start_seconds": "onset_s", "stop_seconds": "ofset_ss"}, ValueError),
        ]
)
def test_columns_map_raise(
        columns_map,
        expected_exception,
        jourjine_et_al_2023_csv_path
):
    with pytest.raises(expected_exception):
        crowsetta.formats.seq.SimpleSeq.from_file(
                annot_path=jourjine_et_al_2023_csv_path,
                columns_map=columns_map,
            )


@pytest.mark.parametrize(
        "default_label",
        [
            None,
            'x',
            '@'
        ]
)
def test_default_label(
    default_label,
    jourjine_et_al_2023_csv_path
    ):
    # test fixes for https://github.com/vocalpy/crowsetta/issues/271
    if default_label is None:
        simple = crowsetta.formats.seq.SimpleSeq.from_file(
            annot_path=jourjine_et_al_2023_csv_path,
            columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s"}
            # we are using default value for `default_label` here
        )
        sig = inspect.signature(crowsetta.SimpleSeq.from_file)
        # replace None with the default value for default label, so assert works below
        default_label = sig.parameters["default_label"].default
    else:
        simple = crowsetta.formats.seq.SimpleSeq.from_file(
            annot_path=jourjine_et_al_2023_csv_path,
            columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s"},
            default_label=default_label
        )

    assert np.array_equal(
        simple.labels, 
        np.array([default_label] * simple.onsets_s.shape[-1])
    )
