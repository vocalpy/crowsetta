import pytest


@pytest.fixture
def birdsong_rec_root(test_data_root):
    """root of data from Birdsong Recognition dataset"""
    return test_data_root / 'koumura'


@pytest.fixture
def birdsong_rec_xml_file(birdsong_rec_root):
    """annotation file from Birdsong Recognition dataset"""
    return birdsong_rec_root / 'Bird0/Annotation.xml'


@pytest.fixture
def birdsong_rec_wavpath(birdsong_rec_root):
    """audio from Birdsong Recognition dataset"""
    return birdsong_rec_root / 'Bird0/Wave'
