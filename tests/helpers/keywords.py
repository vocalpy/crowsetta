import numpy as np


def from_segments(segments):
    labels = []
    onset_samples = []
    offset_samples = []
    onsets_s = []
    offsets_s = []
    for seg in segments:
        labels.append(seg.label)
        onset_samples.append(seg.onset_sample)
        offset_samples.append(seg.offset_sample)
        onsets_s.append(None)
        offsets_s.append(None)
    onset_samples = np.asarray(onset_samples)
    offset_samples = np.asarray(offset_samples)
    onsets_s = np.asarray(onsets_s)
    offsets_s = np.asarray(offsets_s)
    return onset_samples, offset_samples, onsets_s, offsets_s, labels
