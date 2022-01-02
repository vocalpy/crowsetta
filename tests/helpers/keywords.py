import numpy as np


def from_segments(segments):
    labels = []
    onset_inds = []
    offset_inds = []
    onsets_s = []
    offsets_s = []
    for seg in segments:
        labels.append(seg.label)
        onset_inds.append(seg.onset_ind)
        offset_inds.append(seg.offset_ind)
        onsets_s.append(None)
        offsets_s.append(None)
    onset_inds = np.asarray(onset_inds)
    offset_inds = np.asarray(offset_inds)
    onsets_s = np.asarray(onsets_s)
    offsets_s = np.asarray(offsets_s)
    return onset_inds, offset_inds, onsets_s, offsets_s, labels
