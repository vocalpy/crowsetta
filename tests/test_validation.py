import pathlib

import pytest

import crowsetta.validation


@pytest.mark.parametrize(
    "file, extension, raises",
    [
        ("gy6or6/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat", ".not.mat", False),
        (pathlib.Path("gy6or6/032312/gy6or6_baseline_230312_0808.138.cbin.not.mat"), ".not.mat", False),
        ("gy6or6/032312/gy6or6_baseline_230312_0808.138.cbin", ".not.mat", True),
        (pathlib.Path("gy6or6/032312/gy6or6_baseline_230312_0808.138.cbin"), ".not.mat", True),
        ("tests/data_for_tests/koumura/Bird0/Annotation.xml", ".xml", False),
        (pathlib.Path("tests/data_for_tests/koumura/Bird0/Annotation.xml"), ".xml", False),
    ],
)
def test_validate_ext(file, extension, raises):
    if not raises:
        assert crowsetta.validation.validate_ext(file, extension) is None
    else:
        with pytest.raises(ValueError):
            crowsetta.validation.validate_ext(file, extension)
