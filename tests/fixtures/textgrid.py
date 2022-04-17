import pytest

from .data import TEST_DATA_ROOT

TEXTGRID_PATHS = sorted(
        TEST_DATA_ROOT.glob('wav-textgrid/*.TextGrid')
    )


@pytest.fixture
def textgrid_paths():
    return TEXTGRID_PATHS


@pytest.fixture(params=TEXTGRID_PATHS)
def a_textgrid_path(request):
    return request.param
