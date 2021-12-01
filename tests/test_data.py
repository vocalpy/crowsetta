import crowsetta

import pytest


@pytest.mark.parametrize(
    'format',
    list(crowsetta.data.FORMATS.keys())
)
def test_fetch_does_not_fail(format,
                             tmp_path):
        crowsetta.data.fetch(format=format,
                             destination_path=tmp_path)
