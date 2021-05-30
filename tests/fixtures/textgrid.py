import pytest


@pytest.fixture
def textgrids(test_data_root):
    return sorted(
        test_data_root.glob('wav-textgrid/*.TextGrid')
    )


@pytest.fixture
def a_textgrid(textgrids):
    return textgrids[0]
