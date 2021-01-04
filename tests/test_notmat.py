import os
from glob import glob
import tempfile
import shutil
import csv
import unittest
from pathlib import Path, PureWindowsPath

import numpy as np
import evfuncs

import crowsetta

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestNotmat(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(TESTS_DIR, 'test_data')
        self.tmp_output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_notmat2annot_single_str(self):
        notmat = os.path.join(self.test_data_dir,
                              os.path.normpath(
                                  'cbins/gy6or6/032312/'
                                  'gy6or6_baseline_230312_0808.138.cbin.not.mat'))
        annot = crowsetta.notmat.notmat2annot(notmat)
        self.assertTrue(type(annot) == crowsetta.Annotation)
        self.assertTrue(hasattr(annot, 'seq'))

    def test_notmat2annot_list_of_str(self):
        notmat = glob(os.path.join(self.test_data_dir,
                                   os.path.normpath(
                                       'cbins/gy6or6/032312/*.not.mat')))
        annots = crowsetta.notmat.notmat2annot(notmat)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(notmat))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_notmat2annot_list_of_Path(self):
        notmat = sorted(Path(self.test_data_dir).joinpath('cbins/gy6or6/032312/').glob('*.not.mat'))
        annots = crowsetta.notmat.notmat2annot(notmat)
        self.assertTrue(type(annots) == list)
        self.assertTrue(len(annots) == len(list(annots)))
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                            for annot in annots]))

    def test_notmat2csv(self):
        # since notmat_list_to_csv is basically a wrapper around
        # notmat2annot and seq2csv,
        # and those are tested above and in other test modules,
        # here just need to make sure this function doesn't fail
        cbin_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('cbins/gy6or6/032312/'))
        notmat_list = glob(os.path.join(cbin_dir, '*.not.mat'))
        # below, sorted() so it's the same order on different platforms
        notmat_list = sorted(notmat_list)
        csv_filename = os.path.join(str(self.tmp_output_dir),
                                    'test.csv')
        crowsetta.notmat.notmat2csv(notmat_list, csv_filename)
        # make sure file was created
        assert os.path.isfile(csv_filename)

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
        for notmat_name in notmat_list:
            self.assertTrue(
                os.path.basename(notmat_name) in filenames_from_csv
            )

    def test_make_notmat(self):
        cbin_dir = os.path.join(self.test_data_dir,
                                os.path.normpath('cbins/gy6or6/032312/'))
        notmat_list = glob(os.path.join(cbin_dir, '*.not.mat'))
        for notmat in notmat_list:
            notmat_dict = evfuncs.load_notmat(notmat)
            annot = crowsetta.notmat.notmat2annot(notmat, round_times=False)
            seq_dict = annot.seq.as_dict()
            filename = notmat.replace('.not.mat', '')
            crowsetta.notmat.make_notmat(filename=filename,
                                         labels=np.asarray(list(notmat_dict['labels'])),
                                         onsets_s=seq_dict['onsets_s'],
                                         offsets_s=seq_dict['offsets_s'],
                                         samp_freq=notmat_dict['Fs'],
                                         threshold=notmat_dict['threshold'],
                                         min_syl_dur=notmat_dict['min_dur']/1000,
                                         min_silent_dur=notmat_dict['min_int']/1000,
                                         alternate_path=self.tmp_output_dir,
                                         other_vars=None
                                         )
            notmat_made = evfuncs.load_notmat(os.path.join(self.tmp_output_dir,
                                                           os.path.basename(notmat)))
            # can't do assert(new_dict == old_dict)
            # because headers will be different (and we want them to be different)
            for key in ['Fs', 'fname', 'labels', 'onsets', 'offsets',
                        'min_int', 'min_dur', 'threshold', 'sm_win']:
                if key == 'fname':
                    # have to deal with Windows path saved in .not.mat files
                    # and then compare file names without path to them
                    notmat_dict_path = PureWindowsPath(notmat_dict[key])
                    notmat_made_path = Path(notmat_made[key])
                    self.assertTrue(notmat_dict_path.name == notmat_made_path.name)
                elif type(notmat_dict[key]) == np.ndarray:
                    try:
                        self.assertTrue(np.allclose(notmat_dict[key],
                                                    notmat_made[key],
                                                    atol=1e-3, rtol=1e-3))
                    except AssertionError:
                        import pdb;pdb.set_trace()
                else:
                    self.assertTrue(notmat_dict[key] == notmat_made[key])


if __name__ == '__main__':
    unittest.main()
