from pathlib import Path

import pytest

HERE = Path(__file__).parent


@pytest.fixture
def test_data_root():
    """Path that points to root of data_for_tests directory"""
    return HERE.joinpath("..", "data_for_tests")
