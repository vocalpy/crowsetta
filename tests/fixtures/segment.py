import pytest

from crowsetta.segment import Segment


@pytest.fixture
def list_of_segments():
    list_of_segments = []

    for label, onset_sample, offset_sample in zip(("a", "b", "c"), (16000, 32000, 64000), (17000, 33000, 65000)):
        list_of_segments.append(
            Segment(
                label=label,
                onset_sample=onset_sample,
                offset_sample=offset_sample,
            )
        )

    return list_of_segments


@pytest.fixture
def different_list_of_segments():
    list_of_segments = []

    for label, onset_sample, offset_sample in zip(
        ("a", "b", "c", "d"), (16000, 32000, 64000, 128000), (17100, 33100, 65100, 129100)
    ):
        list_of_segments.append(
            Segment(
                label=label,
                onset_sample=onset_sample,
                offset_sample=offset_sample,
            )
        )

    return list_of_segments
