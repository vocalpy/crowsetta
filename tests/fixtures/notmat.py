import pytest


@pytest.fixture
def notmats_root(test_data_root):
    """root of test data for .cbin audio / .not.mat annotation
    as from Bengalese Finch Song Repository dataset"""
    return test_data_root / 'cbins/gy6or6/032312'


@pytest.fixture
def notmats(notmats_root):
    return [
        str(notmat) for notmat in sorted(notmats_root.glob('*.not.mat'))
    ]


@pytest.fixture
def a_notmat(notmats):
    return notmats[0]
