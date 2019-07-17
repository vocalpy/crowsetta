import os
from glob import glob
import tempfile
import shutil
import csv
import unittest
from pathlib import Path

import crowsetta
from crowsetta.segment import Segment

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestTextgrid(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_textgrid2annot_single_str(self):
        textgrid = glob(os.path.join(self.test_data_dir,
                                     os.path.normpath(
                                         'wav-textgrid/*.TextGrid')))
        a_textgrid = textgrid[0]
        annot = crowsetta.textgrid.textgrid2annot(a_textgrid)
        self.assertTrue(type(annot) == crowsetta.Annotation)

    def test_textgrid2annot_list_of_str(self):
        textgrid = glob(os.path.join(self.test_data_dir,
                                     os.path.normpath(
                                         'wav-textgrid/*.TextGrid')))
        annots = crowsetta.textgrid.textgrid2annot(textgrid)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(textgrid))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_textgrid2annot_list_of_Path(self):
        textgrid = Path(self.test_data_dir).joinpath(
            'wav-textgrid').glob('*.TextGrid')
        annots = crowsetta.textgrid.textgrid2annot(textgrid)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(list(textgrid)))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_textgrid2csv(self):
        # since textgrid2csv is basically a wrapper around
        # textgrid2annot and seq2csv,
        # and those are tested above and in other test modules,
        # here just need to make sure this function doesn't fail
        textgrid_dir = os.path.join(self.test_data_dir,
                                    os.path.normpath('wav-textgrid'))
        textgrid_list = glob(os.path.join(textgrid_dir, '*.not.mat'))
        # below, sorted() so it's the same order on different platforms
        textgrid_list = sorted(textgrid_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        crowsetta.textgrid.textgrid2csv(textgrid_list, csv_filename)
        # make sure file was created
        assert os.path.isfile(csv_filename)

        # to be extra sure, make sure all filenames from
        # .TextGrid list are in csv
        filenames_from_csv = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=Segment._FIELDS)
            header = next(reader)
            for row in reader:
                filenames_from_csv.append(row['file'])
        for textgrid_name in textgrid_list:
            wav_name = textgrid_name.replace('.TextGrid', '.wav')
            assert(wav_name in filenames_from_csv)


if __name__ == '__main__':
    unittest.main()
