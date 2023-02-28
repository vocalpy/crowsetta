import pytest

from .data import TEST_DATA_ROOT

NOTMATS_ROOT = TEST_DATA_ROOT / "cbins/gy6or6/032312"


@pytest.fixture
def notmats_root():
    """root of test data for .cbin audio / .not.mat annotation
    as from Bengalese Finch Song Repository dataset"""
    return NOTMATS_ROOT


NOTMATS = sorted(NOTMATS_ROOT.glob("*.not.mat"))


@pytest.fixture
def notmat_paths(notmats_root):
    return NOTMATS


@pytest.fixture(params=NOTMATS)
def a_notmat_path(request):
    return request.param
