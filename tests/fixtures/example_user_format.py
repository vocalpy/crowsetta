import pytest


@pytest.fixture
def example_user_format_root(test_data_root):
    return test_data_root / 'example_user_format'


@pytest.fixture
def example_user_format_script(example_user_format_root):
    return str(
        example_user_format_root / 'example.py'
    )


@pytest.fixture
def example_user_format_annotation_file(example_user_format_root):
    return example_user_format_root / 'bird1_annotation.mat'
