import pytest

from .data import TEST_DATA_ROOT

AUDTXT_PATHS = sorted(
        TEST_DATA_ROOT.glob('aud-txt/giraudon-et-al-2022/audacity-annotations/*.audacity.txt')
    )


@pytest.fixture
def audtxt_paths():
    return AUDTXT_PATHS


@pytest.fixture(params=AUDTXT_PATHS)
def an_audtxt_path(request):
    return request.param
