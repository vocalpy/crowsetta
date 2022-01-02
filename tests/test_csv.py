import sys
import os
import csv
from pathlib import Path
from importlib import import_module

import pytest

import crowsetta

TESTS_DIR = Path(__file__).resolve().parent  # same as os.path.dirname(__file__)


def test_annot2csv(test_data_root, 
                   tmp_path):
    # compare csv created by annot2csv
    # with correctly generated csv saved in crowsetta/tests/test_data_root
    cbin_dir = test_data_root.joinpath('cbins/gy6or6/032312/')
    notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
    # below, sorted() so it's the same order on different platforms
    notmat_list = sorted(notmat_list)
    annot_list = crowsetta.notmat.notmat2annot(notmat_list)
    csv_filename = os.path.join(str(tmp_path),
                                'test.csv')
    # below, set basename to True so we can easily run tests on any system without
    # worrying about where audio files are relative to root of directory tree
    crowsetta.csv.annot2csv(annot_list,
                            csv_filename,
                            basename=True)
    assert os.path.isfile(csv_filename)
    test_rows = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            test_rows.append(row)

    csv_to_compare_with = test_data_root.joinpath('csv/gy6or6_032312.csv')
    compare_rows = []
    with open(csv_to_compare_with, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            compare_rows.append(row)
    for test_row, compare_row in zip(test_rows, compare_rows):
        assert test_row == compare_row


def test_annot2csv_when_one_pair_of_onsets_and_offsets_is_None(tmp_path,
                                                               example_user_format_root,
                                                               example_user_format_annotation_file):
    # example2seq only gets onset and offset times in seconds
    # so onset_ind and offset_ind will be None
    # Test that we can make a csv that has 'None' in columns for
    # onset_ind and offset_ind when they are None for each segment
    sys.path.append(str(example_user_format_root))
    example_module = import_module(name='example')
    sys.path.remove(str(example_user_format_root))

    annot_list = example_module.example2annot(annot_path=example_user_format_annotation_file)
    assert(
        all(
            [seg.onset_ind is None and seg.offset_ind is None
             for annot in annot_list for seg in annot.seq.segments]
        )
    )
    csv_filename = os.path.join(tmp_path,
                             'test_annot2csv_onset_None.csv')
    crowsetta.csv.annot2csv(annot=annot_list, csv_filename=csv_filename)

    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        onset_ind_ind = header.index('onset_ind')
        offset_ind_ind = header.index('offset_ind')
        for row in reader:
            assert row[onset_ind_ind] == 'None' and row[offset_ind_ind] == 'None'


def test_toannot_func_to_csv_with_builtin_format(test_data_root, tmp_path):
    notmat2csv = crowsetta.csv.toannot_func_to_csv(crowsetta.notmat.notmat2annot)
    cbin_dir = test_data_root.joinpath('cbins/gy6or6/032312/')
    notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
    # below, sorted() so it's the same order on different platforms
    notmat_list = sorted(notmat_list)
    csv_filename = os.path.join(tmp_path,
                                'test_toseq_func_to_csv_gy6or6_032312.csv')
    notmat2csv(file=notmat_list,
               csv_filename=csv_filename,
               basename=True)

    test_rows = []
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            test_rows.append(row)

    csv_to_compare_with = test_data_root.joinpath('csv/gy6or6_032312.csv')
    compare_rows = []
    with open(csv_to_compare_with, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            compare_rows.append(row)
    for test_row, compare_row in zip(test_rows, compare_rows):
        assert test_row == compare_row


def test_csv2annot(test_data_root):
    csv_filename = test_data_root.joinpath('csv/gy6or6_032312.csv')
    # convert csv to crowsetta list -- this is what we're testing
    annot_list_from_csv = crowsetta.csv.csv2annot(csv_filename)
    cbin_dir = test_data_root.joinpath('cbins/gy6or6/032312/')

    # get what should be the same seq list from .not.mat files
    # to compare with what we got from the csv
    notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
    # below, sorted() so it's the same order on different platforms
    notmat_list = sorted(notmat_list)
    annot_list_from_notmats = crowsetta.notmat.notmat2annot(notmat_list,
                                                            basename=True)

    # make sure everything is the same in the two annotation lists
    for from_csv, from_notmat in zip(annot_list_from_csv,
                                     annot_list_from_notmats):
        assert from_csv == from_notmat


def test_csv2annot_unrecognized_fields_raises(test_data_root):
    csv_filename = str(
        test_data_root.joinpath('csv/unrecognized_fields_in_header.csv')
    )
    with pytest.raises(ValueError):
        crowsetta.csv.csv2annot(csv_filename=csv_filename)


def test_csv2annot_missing_fields_raises(test_data_root):
    csv_filename = str(
        test_data_root.joinpath('csv/missing_fields_in_header.csv')
    )
    with pytest.raises(ValueError):
        crowsetta.csv.csv2annot(csv_filename=csv_filename)


def test_csv2annot_when_one_pair_of_onsets_and_offsets_is_None(test_data_root):
    # Test that we can load a csv that has 'None' in columns for
    # onset_ind and offset_ind, so that they are None for each segment
    csv_with_None_columns = test_data_root.joinpath(
        'csv/example_annotation_with_onset_inds_offset_inds_None.csv'
    )
    seq = crowsetta.csv.csv2annot(csv_filename=csv_with_None_columns)
    assert (
        seg.onset_ind is None and seg.offset_ind is None
        for a_seq in seq for seg in a_seq.segments
    )
