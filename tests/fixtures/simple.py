import pytest

from .data import TEST_DATA_ROOT

SIMPLE_CSVS = sorted(TEST_DATA_ROOT.glob("simple-csv/hmbg-sound-analysis-workshop/*.csv"))


@pytest.fixture
def simple_csv_paths():
    return SIMPLE_CSVS


@pytest.fixture(params=SIMPLE_CSVS)
def a_simple_csv_path(request):
    return request.param


DAS_CSVS = sorted(TEST_DATA_ROOT.glob("simple-csv/steinfath-et-al-2021/*.csv"))


@pytest.fixture
def das_csv_paths():
    return DAS_CSVS


@pytest.fixture(params=DAS_CSVS)
def a_das_csv_path(request):
    return request.param


@pytest.fixture()
def jourjine_et_al_2023_csv_path():
    return (
        TEST_DATA_ROOT / "simple-csv" / "jourjine-et-al-2023" / 
        "GO_24860x23748_ltr2_pup3_ch4_4800_m_337_295_fr1_p9_2021-10-02_12-35-01.csv"
    )