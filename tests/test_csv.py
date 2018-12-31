import os
import tempfile
import shutil
import csv
import unittest
from pathlib import Path

import numpy as np
import attr

import crowsetta

TESTS_DIR = Path(__file__).resolve().parent  # same as os.path.dirname(__file__)


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = TESTS_DIR.joinpath('test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_seq2csv(self):
        # compare csv created by seq2csv
        # with correctly generated csv saved in crowsetta/tests/test_data
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')
        notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        seq_list = []
        for notmat in notmat_list:
            seq_list.append(crowsetta.notmat.notmat2seq(notmat))
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        # below, set basename to True so we can easily run tests on any system without
        # worrying about where audio files are relative to root of directory tree
        crowsetta.csv.seq2csv(seq_list,
                              csv_filename,
                              basename=True)
        assert os.path.isfile(csv_filename)
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
            assert test_row == compare_row

    def test_toseq_func_to_csv_with_builtin_format(self):
        notmat2csv = crowsetta.csv.toseq_func_to_csv(crowsetta.notmat.notmat2seq)
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')
        notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        csv_fname = os.path.join(self.tmp_output_dir,
                                 'test_toseq_func_to_csv_gy6or6_032312.csv')
        to_csv_kwargs = {'csv_fname': csv_fname,
                         'basename': True}
        notmat2csv(file=notmat_list, to_csv_kwargs=to_csv_kwargs)

        test_rows = []
        with open(csv_fname, 'r', newline='') as csvfile:
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

    def test_csv2seq(self):
        csv_fname = self.test_data_dir.joinpath('csv/gy6or6_032312.csv')
        # convert csv to crowsetta list -- this is what we're testing
        seq_list_from_csv = crowsetta.csv.csv2seq(csv_fname)
        cbin_dir = self.test_data_dir.joinpath('cbins/gy6or6/032312/')

        # get what should be the same seq list from .not.mat files
        # to compare with what we got from the csv
        notmat_list = [str(path) for path in cbin_dir.glob('*.not.mat')]
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        seq_list_from_notmats = []
        for notmat in notmat_list:
            seq_list_from_notmats.append(crowsetta.notmat.notmat2seq(notmat,
                                                                     basename=True))

        # make sure everything is the same in the two annotation lists
        for from_csv, from_notmat in zip(seq_list_from_csv, seq_list_from_notmats):
            from_csv = attr.asdict(from_csv)
            from_notmat = attr.asdict(from_notmat)
            for from_csv_key, from_csv_val in from_csv.items():
                if type(from_csv_val) == str:
                    assert from_csv_val == from_notmat[from_csv_key]
                elif type(from_csv_val) == np.ndarray:
                    # hacky platform-agnostic way to say "if integer"
                    if from_csv_val.dtype == np.asarray(int(1)).dtype:
                        assert np.array_equal(from_csv_val,
                                              from_notmat[from_csv_key])
                    # hacky platform-agnostic way to say "if float"
                    elif from_csv_val.dtype == np.asarray((1.)).dtype:
                        assert np.allclose(from_csv[from_csv_key],
                                           from_notmat[from_csv_key])

    def test_csv2seq_unrecognized_fields_raises(self):
        csv_fname = str(self.test_data_dir.joinpath('csv/unrecognized_fields_in_header.csv'))
        with self.assertRaises(ValueError):
            crowsetta.csv.csv2seq(csv_fname=csv_fname)

    def test_csv2seq_missing_fields_raises(self):
        csv_fname = str(self.test_data_dir.joinpath('csv/missing_fields_in_header.csv'))
        with self.assertRaises(ValueError):
            crowsetta.csv.csv2seq(csv_fname=csv_fname)


if __name__ == '__main__':
    unittest.main()
