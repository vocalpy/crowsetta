import os
from glob import glob
import tempfile
import shutil
import csv
import unittest

import numpy as np

import conbirt

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

ANNOT_DICT_FIELDNAMES = {'filename': str,
                         'onsets_Hz': np.ndarray,
                         'offsets_Hz': np.ndarray,
                         'onsets_s': np.ndarray,
                         'offsets_s': np.ndarray,
                         'labels': np.ndarray}

SYL_DICT_FIELDNAMES = ['filename',
                       'onset_Hz',
                       'offset_Hz',
                       'onset_s',
                       'offset_s',
                       'label']


class TestNotmat(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_notmat2seq(self):
        notmat = os.path.join(self.test_data_dir,
                              os.path.normpath(
                                  'cbins/gy6or6/032312/'
                                  'gy6or6_baseline_230312_0808.138.cbin.not.mat'))
        annot_dict = conbirt.notmat.notmat2seq(notmat)
        for fieldname, fieldtype in ANNOT_DICT_FIELDNAMES.items():
            assert fieldname in annot_dict
            assert type(annot_dict[fieldname]) == fieldtype

    def test_notmat_list_to_csv(self):
        # since notmat_list_to_csv is basically a wrapper around
        # notmat_to_annot_dict and annot_list_to_csv,
        # and those are tested above,
        # here just need to make sure this function doesn't fail
        cbin_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('cbins/gy6or6/032312/'))
        notmat_list = glob(os.path.join(cbin_dir, '*.not.mat'))
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        conbirt.notmat.notmat_list_to_csv(notmat_list, csv_filename)
        # make sure file was created
        assert os.path.isfile(csv_filename)

        # to be extra sure, make sure all filenames from
        # .not.mat list are in csv
        filenames_from_csv = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=SYL_DICT_FIELDNAMES)
            header = next(reader)
            for row in reader:
                filenames_from_csv.append(row['filename'])
        for fname_from_csv in filenames_from_csv:
            assert(fname_from_csv + '.not.mat' in notmat_list)

    def test_make_notmat(self):
        assert False


if __name__ == '__main__':
    unittest.main()
