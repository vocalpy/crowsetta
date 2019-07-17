import sys
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import crowsetta

TESTS_DIR = Path(__file__).resolve().parent  # same as os.path.dirname(__file__)


class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.tmp_output_dir = Path(tempfile.mkdtemp())
        self.test_data_dir = TESTS_DIR.joinpath('test_data')
        self.example_script_dir = TESTS_DIR.joinpath('test_scripts/')

    def tearDown(self):
        shutil.rmtree(self.tmp_output_dir)

    def test_koumura_from_file(self):
        scribe = crowsetta.Transcriber(annot_format='koumura')
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        annots = scribe.from_file(file=xml_file, wavpath=wavpath)
        self.assertTrue(type(annots) == list)
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))

    def test_koumura_to_csv(self):
        scribe = crowsetta.Transcriber(annot_format='koumura')
        xml_file = str(self.test_data_dir.joinpath('koumura/Bird0/Annotation.xml'))
        wavpath = str(self.test_data_dir.joinpath('koumura/Bird0/Wave'))
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=xml_file, wavpath=wavpath, csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_notmat_from_file(self):
        scribe = crowsetta.Transcriber(annot_format='notmat')
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        for notmat in notmats:
            annot = scribe.from_file(file=notmat)
            self.assertTrue(type(annot) == crowsetta.Annotation)

    def test_notmat_to_csv(self):
        scribe = crowsetta.Transcriber(annot_format='notmat')
        notmats = list(str(notmat) 
                       for notmat in self.test_data_dir.joinpath(
            'cbins/gy6or6/032312').glob('*.not.mat')
        )
        csv_filename = str(self.tmp_output_dir.joinpath('Annotation.csv'))
        scribe.to_csv(file=notmats, csv_filename=csv_filename)
        self.assertTrue(Path(csv_filename).is_file())

    def test_example_from_file_name_import(self):
        sys.path.append(str(self.example_script_dir))
        config = {
            'module': 'example',
            'from_file': 'example2annot',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(annot_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        annots = scribe.from_file(mat_file=annotation)
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))
        sys.path.remove(str(self.example_script_dir))

    def test_only_module_and_from_file_required(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'from_file': 'example2annot',
            }
        scribe = crowsetta.Transcriber(annot_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        annots = scribe.from_file(mat_file=annotation)
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))

    def test_example_from_file_path_import(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'from_file': 'example2annot',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(annot_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        annots = scribe.from_file(mat_file=annotation)
        self.assertTrue(all([type(annot) == crowsetta.Annotation
                             for annot in annots]))

    def test_config_wrong_types_raise(self):
        # should raise an error because config should be a dict
        # not list of dicts
        config = list({
                'module': 'example',
                'from_file': 'example2annot',
                'to_csv': 'example2csv',
                'to_format': 'None',
            }
        )
        with self.assertRaises(TypeError):
            crowsetta.Transcriber(config=config)

    def test_missing_keys_in_config_raises(self):
        config = {
            # missing 'module' key
            'from_file': 'example2annot',
            'to_csv': None,
            'to_format': None,
        }

        with self.assertRaises(KeyError):
            crowsetta.Transcriber(annot_format='example', config=config)

        config = {
            'module': 'example',
            # missing 'from_file' key
            'to_csv': None,
            'to_format': None,
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(annot_format='example', config=config)

    def test_extra_keys_in_config_raises(self):
        config = {
            'module': 'example',
            'from_file': 'example2annot',
            'to_csv': 'example2csv',
            'extra': 'key_right_here',
            'to_format': 'None',
        }
        with self.assertRaises(KeyError):
            crowsetta.Transcriber(annot_format='example', config=config)

    def test_call_to_csv_when_None_raises(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'from_file': 'example2annot',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(annot_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        with self.assertRaises(NotImplementedError):
            scribe.to_csv(mat_mat_file=annotation, csv_filename='bad.csv')

    def test_call_to_format_when_None_raises(self):
        config = {
            'module': str(self.example_script_dir.joinpath('example.py')),
            'from_file': 'example2annot',
            'to_csv': None,
            'to_format': None,
        }
        scribe = crowsetta.Transcriber(annot_format='example', config=config)
        annotation = os.path.join(self.test_data_dir,
                                  'example_user_format',
                                  'bird1_annotation.mat')
        with self.assertRaises(NotImplementedError):
            scribe.to_format(mat_mat_file=annotation, to_format='example')


if __name__ == '__main__':
    unittest.main()
