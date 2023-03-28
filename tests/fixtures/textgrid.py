import pytest

from .data import TEST_DATA_ROOT

TEXTGRID_PATHS = sorted(TEST_DATA_ROOT.glob("wav-textgrid/*.TextGrid"))


@pytest.fixture
def textgrid_paths():
    return TEXTGRID_PATHS


@pytest.fixture(params=TEXTGRID_PATHS)
def a_textgrid_path(request):
    return request.param


TEXTGRID_ROOT = TEST_DATA_ROOT / 'textgrid'
PARSE_TEXTGRID_PATHS = TEXTGRID_ROOT.glob('**/*TextGrid')


@pytest.fixture(params=PARSE_TEXTGRID_PATHS)
def a_parse_textgrid_path(request):
    return request.param


TEXTGRIDS_WITH_EMPTY_INTERVALS_PATHS = [
    TEXTGRID_ROOT / path
    for path in (
        'calhoun-et-al-2022/BroadFocusAlofa.TextGrid',
        'parselmouth/the_north_wind_and_the_sun.short.utf8.TextGrid',
        'praatIO/mary.TextGrid'
    )
]
@pytest.fixture(params=TEXTGRIDS_WITH_EMPTY_INTERVALS_PATHS)
def a_textgrid_with_empty_intervals_path(request):
    return request.param


@pytest.fixture(params=(True, False))
def keep_empty(request):
    return request.param
