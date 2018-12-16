import os
from glob import glob
import tempfile
import shutil
import csv
import unittest

import numpy as np

import conbirt

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_seq2csv(self):
        # compare csv created by seq2csv
        # with correctly generated csv saved in conbirt/tests/test_data
        cbin_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('cbins/gy6or6/032312/'))
        notmat_list = glob(os.path.join(cbin_dir, '*.not.mat'))
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        seq_list = []
        for notmat in notmat_list:
            seq_list.append(conbirt.notmat.notmat2seq(notmat))
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        # below, set basename to True so we can easily run tests on any system without
        # worrying about where audio files are relative to root of directory tree
        conbirt.csv.seq2csv(seq_list,
                            csv_filename,
                            basename=True)
        assert os.path.isfile(csv_filename)
        test_rows = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_rows.append(row)

        csv_to_compare_with = os.path.join(self.test_data_dir,
                                           os.path.normpath('csv/gy6or6_032312.csv'))
        compare_rows = []
        with open(csv_to_compare_with, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                compare_rows.append(row)
        for test_row, compare_row in zip(test_rows, compare_rows):
            assert test_row == compare_row

    def test_csv2seqlist(self):
        csv_fname = os.path.join(self.test_data_dir,
                                 os.path.normpath('csv/gy6or6_032312.csv'))
        # convert csv to conbirt list -- this is what we're testing
        seq_list_from_csv = conbirt.csv.csv2seqlist(csv_fname)
        cbin_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('cbins/gy6or6/032312/'))

        # get what should be the same seq list from .not.mat files
        # to compare with what we got from the csv
        notmat_list = glob(os.path.join(cbin_dir, '*.not.mat'))
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        seq_list_from_notmats = []
        for notmat in notmat_list:
            seq_list_from_notmats.append(conbirt.notmat.notmat2seq(notmat,
                                                                   basename=True))

        # make sure everything is the same in the two annotation lists
        for from_csv, from_notmat in zip(seq_list_from_csv, seq_list_from_notmats):
            from_csv = from_csv._asdict()
            from_notmat = from_notmat._asdict()
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


if __name__ == '__main__':
    unittest.main()
