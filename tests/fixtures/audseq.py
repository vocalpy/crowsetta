import pytest

from .data import TEST_DATA_ROOT

AUDSEQ_PATHS = sorted(TEST_DATA_ROOT.glob("aud-seq/giraudon-et-al-2022/audacity-annotations/*.audacity.txt"))


@pytest.fixture
def audseq_paths():
    return AUDSEQ_PATHS


@pytest.fixture(params=AUDSEQ_PATHS)
def an_audseq_path(request):
    return request.param
