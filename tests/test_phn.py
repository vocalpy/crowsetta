import os
from glob import glob
import tempfile
import shutil
import csv
import unittest
from pathlib import Path

import numpy as np

import crowsetta

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestPhn(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_phn2annot_single_str(self):
        phn = os.path.join(self.test_data_dir,
                           os.path.normpath('audio_wav_annot_phn/sa1.phn'))
        annot = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annot) == crowsetta.Annotation)
        self.assertTrue(hasattr(annot, 'seq'))

    def test_phn2annot_list_of_str(self):
        phn = glob(os.path.join(self.test_data_dir,
                                os.path.normpath('audio_wav_annot_phn/*.phn')))
        annots = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(phn))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))

    def test_phn2annot_list_of_Path(self):
        phn = sorted(Path(self.test_data_dir).joinpath('audio_wav_annot_phn/').glob('*.phn'))
        annots = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(list(annots)))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_phn2csv(self):
        # since notmat_list_to_csv is basically a wrapper around
        # notmat2annot and seq2csv,
        # and those are tested above and in other test modules,
        # here just need to make sure this function doesn't fail
        phn_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('audio_wav_annot_phn'))
        phn_list = glob(os.path.join(phn_dir, '*.phn'))
        # below, sorted() so it's the same order on different platforms
        phn_list = sorted(phn_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        crowsetta.phn.phn2csv(phn_list, csv_filename)
        # make sure file was created
        self.assertTrue(os.path.isfile(csv_filename))

        # to be extra sure, make sure all filenames from
        # .not.mat list are in csv
        filenames_from_csv = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile,
                                    fieldnames=crowsetta.csv.CSV_FIELDNAMES)
            header = next(reader)
            for row in reader:
                filenames_from_csv.append(
                    os.path.basename(row['annot_path'])
                )
        for phn_name in phn_list:
            self.assertTrue(
                os.path.basename(phn_name) in filenames_from_csv
            )

    def test_annot2phn(self):
        phn_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('audio_wav_annot_phn'))
        phn_list = glob(os.path.join(phn_dir, '*.phn'))
        # below, sorted() so it's the same order on different platforms
        phn_list = sorted(phn_list)
        for phn in phn_list:
            annot = crowsetta.phn.phn2annot(phn, round_times=False)
            annot_path = Path(self.tmp_output_dir).joinpath(Path(phn).name)
            # copy wav file to tmp_output_dir so we can open the annot
            # need sampling rate from wave file
            shutil.copyfile(src=annot.audio_path, dst=Path(self.tmp_output_dir).joinpath(Path(annot.audio_path.name)))
            crowsetta.phn.annot2phn(annot, annot_path)
            annot_made = crowsetta.phn.phn2annot(annot_path)
            self.assertTrue(np.all(np.equal(annot.seq.onsets_Hz, annot_made.seq.onsets_Hz)))
            self.assertTrue(np.all(np.equal(annot.seq.offsets_Hz, annot_made.seq.offsets_Hz)))
            self.assertTrue(np.all(np.char.equal(annot.seq.labels, annot_made.seq.labels)))

    def test_PHN2annot_single_str(self):
        """same unit-test as above, but here
        test function still works when .phn extension is capitalized
        and audio files are alternate .WAV format"""
        phn = os.path.join(self.test_data_dir,
                           os.path.normpath('audio_WAV_annot_PHN/SA1.PHN'))
        annot = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annot) == crowsetta.Annotation)
        self.assertTrue(hasattr(annot, 'seq'))

    def test_PHN2annot_list_of_str(self):
        """same unit-test as above, but here
        test function still works when .phn extension is capitalized
        and audio files are alternate .WAV format"""
        phn = glob(os.path.join(self.test_data_dir,
                                os.path.normpath('audio_WAV_annot_PHN/*.PHN')))
        annots = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(phn))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))

    def test_PHN2annot_list_of_Path(self):
        """same unit-test as above, but here
        test function still works when .phn extension is capitalized
        and audio files are alternate .WAV format"""
        phn = sorted(Path(self.test_data_dir).joinpath('audio_WAV_annot_PHN/').glob('*.PHN'))
        annots = crowsetta.phn.phn2annot(phn)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(list(annots)))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_PHN2csv(self):
        """same unit-test as above, but here
        test function still works when .phn extension is capitalized
        and audio files are alternate .WAV format"""
        # since notmat_list_to_csv is basically a wrapper around
        # notmat2annot and seq2csv,
        # and those are tested above and in other test modules,
        # here just need to make sure this function doesn't fail
        phn_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('audio_WAV_annot_PHN'))
        phn_list = glob(os.path.join(phn_dir, '*.PHN'))
        # below, sorted() so it's the same order on different platforms
        phn_list = sorted(phn_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        crowsetta.phn.phn2csv(phn_list, csv_filename)
        # make sure file was created
        self.assertTrue(os.path.isfile(csv_filename))

        # to be extra sure, make sure all filenames from
        # .not.mat list are in csv
        filenames_from_csv = []
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile,
                                    fieldnames=crowsetta.csv.CSV_FIELDNAMES)
            header = next(reader)
            for row in reader:
                filenames_from_csv.append(
                    os.path.basename(row['annot_path'])
                )
        for phn_name in phn_list:
            self.assertTrue(
                os.path.basename(phn_name) in filenames_from_csv
            )

    def test_annot2PHN(self):
        """same unit-test as above, but here
        test function still works when .phn extension is capitalized
        and audio files are alternate .WAV format"""
        phn_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('audio_WAV_annot_PHN'))
        phn_list = glob(os.path.join(phn_dir, '*.PHN'))
        # below, sorted() so it's the same order on different platforms
        phn_list = sorted(phn_list)
        for phn in phn_list:
            annot = crowsetta.phn.phn2annot(phn, round_times=False)
            annot_path = Path(self.tmp_output_dir).joinpath(Path(phn).name)
            # copy wav file to tmp_output_dir so we can open the annot
            # need sampling rate from wave file
            shutil.copyfile(src=annot.audio_path, dst=Path(self.tmp_output_dir).joinpath(Path(annot.audio_path.name)))
            crowsetta.phn.annot2phn(annot, annot_path)
            annot_made = crowsetta.phn.phn2annot(annot_path)
            self.assertTrue(np.all(np.equal(annot.seq.onsets_Hz, annot_made.seq.onsets_Hz)))
            self.assertTrue(np.all(np.equal(annot.seq.offsets_Hz, annot_made.seq.offsets_Hz)))
            self.assertTrue(np.all(np.char.equal(annot.seq.labels, annot_made.seq.labels)))


if __name__ == '__main__':
    unittest.main()
