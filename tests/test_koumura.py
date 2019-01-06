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


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data',
                                          'koumura', 'Bird0')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_koumura2seq(self):
        xml_file = os.path.join(self.test_data_dir, 'Annotation.xml')
        seq_list = crowsetta.koumura.koumura2seq(xml_file=xml_file,
                                                 concat_seqs_into_songs=True,
                                                 wavpath=os.path.join(self.test_data_dir,
                                                                      'Wave'))
        self.assertTrue(type(seq_list) == list)
        self.assertTrue(all([type(seq) == crowsetta.classes.Sequence
                             for seq in seq_list]))

    def test_koumura2csv(self):
        # since koumura2csv is basically a wrapper around
        # koumura2seq and seq2csv,
        # and those are tested above and in other test modules,
        # here just need to make sure this function doesn't fail
        xml_file = os.path.join(self.test_data_dir, 'Annotation.xml')
        wavpath = os.path.join(self.test_data_dir, 'Wave')
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        crowsetta.koumura.koumura2csv(xml_file=xml_file,
                                      wavpath=wavpath,
                                      csv_filename=csv_filename,
                                      basename=True)
        # make sure file was created
        assert os.path.isfile(csv_filename)

        # to be extra sure, make sure all .wav files filenames from are in csv
        filenames_from_csv = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=Segment._FIELDS)
            header = next(reader)
            for row in reader:
                filenames_from_csv.append(row['file'])

        wav_list = glob(os.path.join(self.test_data_dir, 'Wave', '*.wav'))
        wav_list = [Path(wav_file).name for wav_file in wav_list]
        for wav_file in wav_list:
            assert(wav_file in filenames_from_csv)


if __name__ == '__main__':
    unittest.main()
