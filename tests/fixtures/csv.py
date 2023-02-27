import pytest

from .data import TEST_DATA_ROOT

# define all these as constants outside fixtures
# in case we need to access them outside fixtures later,
# e.g.  to parameterize a single fixture ``all_csvs``
CSV_ROOT = TEST_DATA_ROOT / "csv"


@pytest.fixture
def csv_root():
    return CSV_ROOT


NOTMAT_AS_GENERIC_SEQ_CSV = CSV_ROOT / "notmat_gy6or6_032312.csv"


@pytest.fixture
def notmat_as_generic_seq_csv():
    return NOTMAT_AS_GENERIC_SEQ_CSV


BIRDSONGREC_AS_GENERIC_SEQ_CSV = CSV_ROOT / "birdsongrec_Bird0_Annotation.csv"


@pytest.fixture
def birdsongrec_as_generic_seq_csv():
    return BIRDSONGREC_AS_GENERIC_SEQ_CSV


TIMIT_PHN_AS_GENERIC_SEQ_CSV = CSV_ROOT / "timit-dr1-fvmh0-phn.csv"


@pytest.fixture
def timit_phn_as_generic_seq_csv():
    return TIMIT_PHN_AS_GENERIC_SEQ_CSV


EXAMPLE_CUSTOM_FORMAT_AS_GENERIC_SEQ_CSV = CSV_ROOT / "example_custom_format.csv"


@pytest.fixture
def example_user_format_as_generic_seq_csv():
    return EXAMPLE_CUSTOM_FORMAT_AS_GENERIC_SEQ_CSV


CSV_MISSING_FIELDS_IN_HEADER = CSV_ROOT / "missing_fields_in_header.csv"


@pytest.fixture
def csv_missing_fields_in_header():
    return CSV_MISSING_FIELDS_IN_HEADER


CSV_WITH_INVALID_FIELDS_IN_HEADER = CSV_ROOT / "invalid_fields_in_header.csv"


@pytest.fixture
def csv_with_invalid_fields_in_header():
    return CSV_WITH_INVALID_FIELDS_IN_HEADER


CSV_WITH_ONSET_S_BUT_NO_OFFSET_S = CSV_ROOT / "onset_s_column_but_no_offset_s_column.csv"


@pytest.fixture
def csv_with_onset_s_but_no_offset_s():
    return CSV_WITH_ONSET_S_BUT_NO_OFFSET_S


CSV_WITH_ONSET_IND_BUT_NO_OFFSET_IND = CSV_ROOT / "onset_sample_column_but_no_offset_sample_column.csv"


@pytest.fixture
def csv_with_onset_sample_but_no_offset_sample():
    return CSV_WITH_ONSET_IND_BUT_NO_OFFSET_IND


CSV_WITH_NO_ONSET_OR_OFFSET_COLUMN = CSV_ROOT / "no_onset_or_offset_column.csv"


@pytest.fixture
def csv_with_no_onset_or_offset_column():
    return CSV_WITH_NO_ONSET_OR_OFFSET_COLUMN
