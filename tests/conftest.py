import pytest

import crowsetta

from .fixtures import *


@pytest.fixture(autouse=True)
def add_crowsetta(doctest_namespace):
    doctest_namespace["crowsetta"] = crowsetta
