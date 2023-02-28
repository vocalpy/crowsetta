"""fixtures for birdsong-recognition-dataset"""
import pytest

from .data import TEST_DATA_ROOT

BIRDSONG_REC_ROOT = TEST_DATA_ROOT / "birdsongrec"


@pytest.fixture
def birdsong_rec_root():
    """root of data from Birdsong Recognition dataset"""
    return BIRDSONG_REC_ROOT


@pytest.fixture
def birdsong_rec_xml_file():
    """annotation file from Birdsong Recognition dataset"""
    return BIRDSONG_REC_ROOT / "Bird0/Annotation.xml"


@pytest.fixture
def birdsong_rec_wav_path():
    """audio from Birdsong Recognition dataset"""
    return BIRDSONG_REC_ROOT / "Bird0/Wave"
