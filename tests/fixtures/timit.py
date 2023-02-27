"""fixtures for TIMIT dataset"""
import pytest

from .data import TEST_DATA_ROOT

TIMIT_KAGGLE_ROOT = TEST_DATA_ROOT / "timit_kaggle"


@pytest.fixture
def timit_kaggle_root(test_data_root):
    return TIMIT_KAGGLE_ROOT


KAGGLE_PHN_PATHS = sorted(TIMIT_KAGGLE_ROOT.glob("**/*.phn"))


@pytest.fixture
def kaggle_phn_paths():
    return KAGGLE_PHN_PATHS


@pytest.fixture(params=KAGGLE_PHN_PATHS)
def a_kaggle_phn_path(request):
    return request.param


KAGGLE_WRD_PATHS = sorted(TIMIT_KAGGLE_ROOT.glob("**/*.wrd"))


@pytest.fixture(params=KAGGLE_WRD_PATHS)
def a_kaggle_wrd_path(request):
    return request.param


TIMIT_NIST_ROOT = TEST_DATA_ROOT / "timit_nist"


@pytest.fixture
def timit_nist_root():
    return TIMIT_NIST_ROOT


NIST_PHN_PATHS = sorted(TIMIT_NIST_ROOT.glob("**/*.PHN"))


@pytest.fixture(params=NIST_PHN_PATHS)
def a_nist_phn_path(request):
    return request.param


NIST_WRD_PATHS = sorted(TIMIT_NIST_ROOT.glob("**/*.WRD"))


@pytest.fixture(params=NIST_WRD_PATHS)
def a_nist_wrd_path(request):
    return request.param


ALL_PHN_PATHS = KAGGLE_PHN_PATHS + NIST_PHN_PATHS


@pytest.fixture(params=ALL_PHN_PATHS)
def a_phn_path(request):
    return request.param


ALL_WRD_PATHS = KAGGLE_WRD_PATHS + NIST_WRD_PATHS


@pytest.fixture(params=ALL_WRD_PATHS)
def a_wrd_path(request):
    return request.param


ALL_TRANSCRIPT_PATHS = ALL_PHN_PATHS + ALL_WRD_PATHS


@pytest.fixture(params=ALL_TRANSCRIPT_PATHS)
def a_transcript_path(request):
    return request.param
