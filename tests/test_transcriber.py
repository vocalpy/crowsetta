import sys

import crowsetta
import pytest


def test_birdsongrec_from_file(birdsong_rec_xml_file,
                               birdsong_rec_wavpath):
    scribe = crowsetta.Transcriber(format='birdsong-recognition-dataset')
    annots = scribe.from_file(annot_path=birdsong_rec_xml_file,
                              wavpath=birdsong_rec_wavpath)
    assert type(annots) == list
    assert all([type(annot) == crowsetta.Annotation
                for annot in annots])


def test_birdsongrec_to_csv(tmp_path,
                            birdsong_rec_xml_file,
                            birdsong_rec_wavpath):
    scribe = crowsetta.Transcriber(format='birdsong-recognition-dataset')
    csv_filename = tmp_path / 'Annotation.csv'
    scribe.to_csv(annot_path=birdsong_rec_xml_file,
                  wavpath=birdsong_rec_wavpath,
                  csv_filename=csv_filename)
    assert csv_filename.exists()


def test_notmat_from_file(notmats):
    scribe = crowsetta.Transcriber(format='notmat')
    for notmat in notmats:
        annot = scribe.from_file(annot_path=notmat)
        assert type(annot) == crowsetta.Annotation


def test_notmat_to_csv(notmats, tmp_path):
    scribe = crowsetta.Transcriber(format='notmat')
    csv_filename = tmp_path / 'Annotation.csv'
    scribe.to_csv(annot_path=notmats, csv_filename=csv_filename)
    assert csv_filename.exists()


def test_yarden_from_file(yarden_annot_mat):
    scribe = crowsetta.Transcriber(format='yarden')
    annots = scribe.from_file(annot_path=yarden_annot_mat)
    assert type(annots) == list
    assert all([type(annot) == crowsetta.Annotation
                for annot in annots])


def test_yarden_to_csv(tmp_path,
                       yarden_annot_mat):
    scribe = crowsetta.Transcriber(format='yarden')
    csv_filename = tmp_path / 'Annotation.csv'
    scribe.to_csv(annot_path=yarden_annot_mat,
                  csv_filename=csv_filename)
    assert csv_filename.exists()


def test_example_from_file_name_import(example_user_format_root,
                                       example_user_format_annotation_file):
    sys.path.append(str(example_user_format_root))
    config = {
        'module': 'example',
        'from_file': 'example2annot',
        'to_csv': None,
        'to_format': None,
    }
    scribe = crowsetta.Transcriber(format='example', config=config)
    sys.path.remove(str(example_user_format_root))  # not sure we need to do this but jic
    annots = scribe.from_file(annot_path=example_user_format_annotation_file)
    assert all([type(annot) == crowsetta.Annotation
                         for annot in annots])


def test_only_module_and_from_file_required(example_user_format_script,
                                            example_user_format_annotation_file):
    config = {
        'module': str(example_user_format_script),
        'from_file': 'example2annot',
        }
    scribe = crowsetta.Transcriber(format='example', config=config)
    annots = scribe.from_file(annot_path=example_user_format_annotation_file)
    assert all([type(annot) == crowsetta.Annotation
                for annot in annots])


def test_example_from_file_path_import(example_user_format_script,
                                       example_user_format_annotation_file):
    config = {
        'module': example_user_format_script,
        'from_file': 'example2annot',
        'to_csv': None,
        'to_format': None,
    }
    scribe = crowsetta.Transcriber(format='example', config=config)
    annots = scribe.from_file(annot_path=example_user_format_annotation_file)
    assert all([type(annot) == crowsetta.Annotation
                         for annot in annots])


def test_config_wrong_types_raise():
    # should raise an error because config should be a dict
    # not list of dicts
    config = list({
            'module': 'example',
            'from_file': 'example2annot',
            'to_csv': 'example2csv',
            'to_format': 'None',
        }
    )
    with pytest.raises(TypeError):
        crowsetta.Transcriber(config=config)


def test_missing_keys_in_config_raises():
    config = {
        # missing 'module' key
        'from_file': 'example2annot',
        'to_csv': None,
        'to_format': None,
    }

    with pytest.raises(KeyError):
        crowsetta.Transcriber(format='example', config=config)

    config = {
        'module': 'example',
        # missing 'from_file' key
        'to_csv': None,
        'to_format': None,
    }
    with pytest.raises(KeyError):
        crowsetta.Transcriber(format='example', config=config)


def test_extra_keys_in_config_raises():
    config = {
        'module': 'example',
        'from_file': 'example2annot',
        'to_csv': 'example2csv',
        'extra': 'key_right_here',
        'to_format': 'None',
    }
    with pytest.raises(KeyError):
        crowsetta.Transcriber(format='example', config=config)


def test_call_to_csv_when_None_raises(example_user_format_script,
                                      example_user_format_annotation_file):
    config = {
        'module': example_user_format_script,
        'from_file': 'example2annot',
        'to_csv': None,
        'to_format': None,
    }
    scribe = crowsetta.Transcriber(format='example', config=config)
    with pytest.raises(NotImplementedError):
        scribe.to_csv(mat_file=example_user_format_annotation_file,
                      csv_filename='bad.csv')


def test_call_to_format_when_None_raises(example_user_format_script,
                                         example_user_format_annotation_file):
    config = {
        'module': example_user_format_script,
        'from_file': 'example2annot',
        'to_csv': None,
        'to_format': None,
    }
    scribe = crowsetta.Transcriber(format='example', config=config)
    with pytest.raises(NotImplementedError):
        scribe.to_format(annot_path=example_user_format_annotation_file, to_format='example')
