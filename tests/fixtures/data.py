from pathlib import Path

import pytest

HERE = Path(__file__).parent
TEST_DATA_ROOT = HERE.joinpath("..", "data_for_tests")


@pytest.fixture
def test_data_root():
    """Path that points to root of data_for_tests directory"""
    return TEST_DATA_ROOT
