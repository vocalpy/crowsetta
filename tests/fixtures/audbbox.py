import pytest

from .data import TEST_DATA_ROOT

AUDBBOX_PATHS = sorted(TEST_DATA_ROOT.glob("aud-bbox/*.txt"))


@pytest.fixture
def audbbox_paths():
    return AUDBBOX_PATHS


@pytest.fixture(params=AUDBBOX_PATHS)
def an_audbbox_path(request):
    return request.param
