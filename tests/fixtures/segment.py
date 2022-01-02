import pytest

from crowsetta.segment import Segment


@pytest.fixture
def list_of_segments():
    list_of_segments = []

    for label, onset_ind, offset_ind in zip(
            ('a', 'b', 'c'),
            (16000, 32000, 64000),
            (17000, 33000, 65000)
    ):
        list_of_segments.append(
            Segment.from_keyword(
                label=label,
                onset_ind=onset_ind,
                offset_ind=offset_ind,
            )
        )

    return list_of_segments


@pytest.fixture
def different_list_of_segments():
    list_of_segments = []

    for label, onset_ind, offset_ind in zip(
            ('a', 'b', 'c', 'd'),
            (16000, 32000, 64000, 128000),
            (17100, 33100, 65100, 129100)
    ):
        list_of_segments.append(
            Segment.from_keyword(
                label=label,
                onset_ind=onset_ind,
                offset_ind=offset_ind,
            )
        )

    return list_of_segments
