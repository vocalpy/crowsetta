import pytest

from .data import TEST_DATA_ROOT

RAVEN_ROOT = TEST_DATA_ROOT / "raven"


@pytest.fixture
def raven_root():
    """root of data from Birdsong Recognition dataset"""
    return RAVEN_ROOT


ALL_RAVEN_TXT_FILES = sorted(RAVEN_ROOT.joinpath("chronister-at-al-2021/Annotation_Files/Recording_1").glob("*.txt"))
# skip first file because it has no annotated rows
# (but keep it to use for testing error handling)
RAVEN_TXT_FILE_WITH_NO_ROWS = ALL_RAVEN_TXT_FILES[0]
RAVEN_TXT_FILES = ALL_RAVEN_TXT_FILES[1:]


@pytest.fixture
def raven_txt_files():
    """Raven .txt annotation files"""
    return RAVEN_TXT_FILES


@pytest.fixture(params=RAVEN_TXT_FILES)
def a_raven_txt_file(request):
    return request.param


@pytest.fixture
def raven_dataset_annot_col():
    return "Species"


@pytest.fixture
def raven_txt_file_with_no_rows():
    return RAVEN_TXT_FILE_WITH_NO_ROWS
