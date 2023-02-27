import numpy as np
import pytest

import crowsetta


@pytest.fixture
def a_bboxes_list():
    bboxes = []
    onsets = np.linspace(0.5, 10, 10)
    offsets = onsets + 0.25
    low_freqs = np.ones_like(onsets) * 500.0
    high_freqs = np.ones_like(offsets) * 12500.0
    labels = np.array(["a"] * onsets.shape[0])
    for onset, offset, low_freq, high_freq, label in zip(onsets, offsets, low_freqs, high_freqs, labels):
        bboxes.append(crowsetta.BBox(onset=onset, offset=offset, low_freq=low_freq, high_freq=high_freq, label=label))
    return bboxes
