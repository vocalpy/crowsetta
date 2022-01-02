import pytest

from crowsetta.sequence import Sequence

from ..helpers import keywords


@pytest.fixture
def a_seq(list_of_segments):
    (onset_inds,
     offset_inds,
     onsets_s,
     offsets_s,
     labels) = keywords.from_segments(list_of_segments)

    a_seq = Sequence(segments=list_of_segments,
                     onset_inds=onset_inds,
                     offset_inds=offset_inds,
                     onsets_s=onsets_s,
                     offsets_s=offsets_s,
                     labels=labels,
                     )
    return  a_seq


@pytest.fixture
def same_seq(list_of_segments):
    (onset_inds,
     offset_inds,
     onsets_s,
     offsets_s,
     labels) = keywords.from_segments(list_of_segments)

    same_seq = Sequence(segments=list_of_segments,
                        onset_inds=onset_inds,
                        offset_inds=offset_inds,
                        onsets_s=onsets_s,
                        offsets_s=offsets_s,
                        labels=labels,
                        )
    return same_seq


@pytest.fixture
def different_seq(different_list_of_segments):
    (onset_inds,
     offset_inds,
     onsets_s,
     offsets_s,
     labels) = keywords.from_segments(different_list_of_segments)

    different_seq = Sequence(segments=different_list_of_segments,
                             onset_inds=onset_inds,
                             offset_inds=offset_inds,
                             onsets_s=onsets_s,
                             offsets_s=offsets_s,
                             labels=labels,
                             )

    return different_seq