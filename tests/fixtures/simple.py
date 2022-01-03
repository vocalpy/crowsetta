import pytest


@pytest.fixture
def simple_csvs(test_data_root):
    return sorted(
        test_data_root.glob('simple-csv/*.csv')
    )


@pytest.fixture
def a_simple_csv(simple_csvs):
    return simple_csvs[0]
