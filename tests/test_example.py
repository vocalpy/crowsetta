import pathlib

import pytest

import crowsetta

@pytest.fixture(params=[False, True, None])
def return_path(request):
    return request.param

@pytest.mark.parametrize(
        'example',
        crowsetta.examples._examples.EXAMPLES
)
def test_example(example, return_path):
    # this is basically a smoke test, 
    # that tests whether we can iterate through all examples
    # without an error
    if return_path is not None:
        out = crowsetta.example(example.name, return_path=return_path)
    else:
         out = crowsetta.example(example.name)

    if return_path is True:
        assert isinstance(out, pathlib.Path)
    else:
        assert isinstance(
            out,
            crowsetta.formats.FORMATS[example.format]
        )
