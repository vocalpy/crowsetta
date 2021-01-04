import sys
import os
import tempfile
import shutil
import csv
import unittest
from pathlib import Path
from importlib import import_module

import crowsetta

TESTS_DIR = Path(__file__).resolve().parent  # same as os.path.dirname(__file__)


class TestCSV(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = TESTS_DIR.joinpath('test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_annot2csv(self):
        # compare csv created by annot2csv
        # with correctly generated csv saved in crowsetta/tests/test_data
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')
        notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        annot_list = crowsetta.notmat.notmat2annot(notmat_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        # below, set basename to True so we can easily run tests on any system without
        # worrying about where audio files are relative to root of directory tree
        crowsetta.csv.annot2csv(annot_list,
                                csv_filename,
                                basename=True)
        self.assertTrue(os.path.isfile(csv_filename))
        test_rows = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_rows.append(row)

        csv_to_compare_with = self.test_data_dir.joinpath('csv/gy6or6_032312.csv')
        compare_rows = []
        with open(csv_to_compare_with, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                compare_rows.append(row)
        for test_row, compare_row in zip(test_rows, compare_rows):
            self.assertTrue(test_row == compare_row)

    def test_annot2csv_when_one_pair_of_onsets_and_offsets_is_None(self):
        # example2seq only gets onset and offset times in seconds
        # so onset_Hz and offset_Hz will be None
        # Test that we can make a csv that has 'None' in columns for
        # onset_Hz and offset_Hz when they are None for each segment

        # first load the module with example2seq
        example_script_dir = TESTS_DIR.joinpath('test_scripts/')
        sys.path.append(str(example_script_dir))
        example_module = import_module(name='example')

        annot_path = str(self.test_data_dir.joinpath(
            'example_user_format/bird1_annotation.mat')
        )
        annot_list = example_module.example2annot(annot_path=annot_path)
        self.assertTrue(
            all(
                [seg.onset_Hz is None and seg.offset_Hz is None
                 for annot in annot_list for seg in annot.seq.segments]
            )
        )
        csv_filename = os.path.join(self.tmp_output_dir,
                                 'test_annot2csv_onset_None.csv')
        crowsetta.csv.annot2csv(annot=annot_list, csv_filename=csv_filename)

        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            onset_Hz_ind = header.index('onset_Hz')
            offset_Hz_ind = header.index('offset_Hz')
            for row in reader:
                self.assertTrue(
                    row[onset_Hz_ind] == 'None' and row[offset_Hz_ind] == 'None'
                )

        sys.path.remove(str(example_script_dir))

    def test_toannot_func_to_csv_with_builtin_format(self):
        notmat2csv = crowsetta.csv.toannot_func_to_csv(crowsetta.notmat.notmat2annot)
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')
        notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        csv_filename = os.path.join(self.tmp_output_dir,
                                 'test_toseq_func_to_csv_gy6or6_032312.csv')
        notmat2csv(file=notmat_list,
                   csv_filename=csv_filename,
                   basename=True)

        test_rows = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_rows.append(row)

        csv_to_compare_with = self.test_data_dir.joinpath('csv/gy6or6_032312.csv')
        compare_rows = []
        with open(csv_to_compare_with, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                compare_rows.append(row)
        for test_row, compare_row in zip(test_rows, compare_rows):
            self.assertTrue(test_row == compare_row)

    def test_csv2annot(self):
        csv_filename = self.test_data_dir.joinpath('csv/gy6or6_032312.csv')
        # convert csv to crowsetta list -- this is what we're testing
        annot_list_from_csv = crowsetta.csv.csv2annot(csv_filename)
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')

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
            self.assertTrue(
                from_csv == from_notmat
            )

    def test_csv2annot_unrecognized_fields_raises(self):
        csv_filename = str(
            self.test_data_dir.joinpath('csv/unrecognized_fields_in_header.csv')
        )
        with self.assertRaises(ValueError):
            crowsetta.csv.csv2annot(csv_filename=csv_filename)

    def test_csv2annot_missing_fields_raises(self):
        csv_filename = str(
            self.test_data_dir.joinpath('csv/missing_fields_in_header.csv')
        )
        with self.assertRaises(ValueError):
            crowsetta.csv.csv2annot(csv_filename=csv_filename)

    def test_csv2annot_when_one_pair_of_onsets_and_offsets_is_None(self):
        # Test that we can load a csv that has 'None' in columns for
        # onset_Hz and offset_Hz, so that they are None for each segment
        csv_with_None_columns = self.test_data_dir.joinpath(
            'csv/example_annotation_with_onsets_Hz_offsets_Hz_None.csv'
        )
        seq = crowsetta.csv.csv2annot(csv_filename=csv_with_None_columns)
        self.assertTrue(
            seg.onset_Hz is None and seg.offset_Hz is None
            for a_seq in seq for seg in a_seq.segments
        )


if __name__ == '__main__':
    unittest.main()
