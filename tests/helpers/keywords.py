import numpy as np


def from_segments(segments):
    labels = []
    onsets_Hz = []
    offsets_Hz = []
    onsets_s = []
    offsets_s = []
    for seg in segments:
        labels.append(seg.label)
        onsets_Hz.append(seg.onset_Hz)
        offsets_Hz.append(seg.offset_Hz)
        onsets_s.append(None)
        offsets_s.append(None)
    onsets_Hz = np.asarray(onsets_Hz)
    offsets_Hz = np.asarray(offsets_Hz)
    onsets_s = np.asarray(onsets_s)
    offsets_s = np.asarray(offsets_s)
    return onsets_Hz, offsets_Hz, onsets_s, offsets_s, labels
