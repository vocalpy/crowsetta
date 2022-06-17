---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
file_format: mystnb
mystnb:
  execution_mode: 'off'
---

```{code-cell} ipython3
import pathlib

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pyprojroot

import crowsetta
```

```{code-cell} ipython3
def plot_spect(S_db, sr, ylim=None, 
               hop_length=512, win_length=512, x_coords=None,
               figsize=(10, 4), dpi=300, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, win_length=win_length, 
                                   x_coords=x_coords, y_axis='linear', x_axis='time', ax=ax)

    if ylim:
        ax.set_ylim(ylim)
```

```{code-cell} ipython3
def plot_labels(labels,
                t,
                t_shift_label=0.01,
                y=0.4,
                ax=None,
                text_kwargs=None):
    """plot labels on an axis.

    Parameters
    ----------
    labels : list, numpy.ndarray
    t : numpy.ndarray
        times (in seconds) at which to plot labels
    t_shift_label : float
        amount (in seconds) that labels should be shifted to the left, for centering.
        Necessary because width of text box isn't known until rendering.
    y : float, int
        height on y-axis at which segments should be plotted.
        Default is 0.5.
    ax : matplotlib.axes.Axes
        axes on which to plot segment. Default is None,
        in which case a new Axes instance is created
    text_kwargs : dict
        keyword arguments passed to the `Axes.text` method
        that plots the labels. Default is None.

    Returns
    -------
    text_list : list
        of text objections, the matplotlib.Text instances for each label
    """
    if text_kwargs is None:
        text_kwargs = {}

    if ax is None:
        fig, ax = plt.subplots

    text_list = []    
    
    for label, t_lbl in zip(labels, t):
        t_lbl -= t_shift_label
        text = ax.text(t_lbl, y, label, **text_kwargs, label='label')
        text_list.append(text)
    
    return text_list
```

```{code-cell} ipython3
def plot_segments(
    annot,
    label_color_map,
    ax,
    tlim=None,
    y_segments=0.4,
    h_segments=0.4,
    y_labels=0.3,
    text_kwargs=None
):
    rectangles = []

    labels = []
    onsets = []
    offsets = []
    for seg in annot.seq.segments:
        label, onset_s, offset_s = seg.label, seg.onset_s, seg.offset_s
        if tlim:
            if offset_s < tlim[0] or onset_s > tlim[1]:
                continue
        labels.append(label)
        onsets.append(onset_s)
        offsets.append(offset_s)
    
    labels = np.array(labels)
    onsets = np.array(onsets)
    offsets = np.array(offsets)
    
    for label, onset_s, offset_s in zip(labels, onsets, offsets):
        rectangle = plt.Rectangle(
            (onset_s, y_segments), 
            width=offset_s - onset_s,
            height=h_segments,
            facecolor=label_color_map[label]
        )
        ax.add_patch(rectangle)
        rectangles.append(rectangle)
    
    t = onsets + ((offsets - onsets) / 2)
    plot_labels(labels, t=t, y=y_labels, text_kwargs=text_kwargs, ax=ax)

    if tlim:
        ax.set_xlim(tlim)

    return rectangles
```

```{code-cell} ipython3
SCRIPTS_ROOT = pyprojroot.here() / 'doc/scripts'

WAV_PATH = SCRIPTS_ROOT / 'audio' / 'b06_concat-snippet.wav'
TG_PATH = SCRIPTS_ROOT / 'annot' / 'b06_concat_dtw.TextGrid'

STATIC_ROOT = pyprojroot.here() / 'doc/_static'
FIG_PATH = STATIC_ROOT / 'example-textgrid-for-index.png'
```

```{code-cell} ipython3
tg = crowsetta.formats.by_name('textgrid').from_file(TG_PATH)
annot = tg.to_annot()

labelset = set(
    [segment.label for segment in annot.seq.segments]
)
cmap = plt.cm.get_cmap('tab20')
colors = [cmap(ind) for ind in range(len(labelset))]
label_color_map = {label: color for label, color in zip(labelset, colors)}
```

```{code-cell} ipython3
FS = 32000  # original file sampling rate
# we need original start and stop times,
# so we can show them on x-axis, and so 
# we know what segment annotations to plot
TLIM_S_ORIGINAL = [5.8, 8.05]  
TLIM_INDS = [int(t * FS) for t in TLIM_S_ORIGINAL]
assert TLIM_INDS == [185600, 257600]

# we also need this to compute "tlim" from the saved clip
CLIP_INDS = [184000, 259000]
CLIP_S_ORIGINAL = [ind / FS for ind in CLIP_INDS]

tlim_inds_snippet = [tlim_ind - CLIP_INDS[0] for tlim_ind in TLIM_INDS]
```

```{code-cell} ipython3
hop_length=256
win_length=512

y, sr = librosa.load(WAV_PATH, sr=None)  # sr=None to keep original sampling rate
y = y[tlim_inds_snippet[0]:tlim_inds_snippet[1]]

D = librosa.stft(y, hop_length=hop_length, win_length=win_length)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

idx = np.array(range(0, S_db.shape[1]))
x_coords = librosa.frames_to_time(idx, sr=sr, hop_length=hop_length, n_fft=2048)
x_coords = x_coords + TLIM_S_ORIGINAL[0]
```

```{code-cell} ipython3
FONT_SIZE = 14

plt.rc('font', size=FONT_SIZE)
plt.rc('axes', labelsize=FONT_SIZE)
plt.rc('xtick', labelsize=FONT_SIZE)
plt.rc('ytick', labelsize=FONT_SIZE)

fig = plt.figure(constrained_layout=True, figsize=(10, 6), dpi=300)
gs = fig.add_gridspec(5, 1)
ax_arr = []
ax_arr.append(
    fig.add_subplot(gs[:3,:])
)
ax_arr.append(
    fig.add_subplot(gs[3:,:])
)

ax_arr = np.array(ax_arr)

plot_spect(S_db, sr, 
           hop_length=hop_length, win_length=win_length, 
           x_coords=x_coords,
           ylim=[128, 11000], ax=ax_arr[0])


_ = plot_segments(annot=annot, label_color_map=label_color_map, 
                  text_kwargs={'fontsize': FONT_SIZE}, ax=ax_arr[1], tlim=TLIM_S_ORIGINAL)

ax_arr[1].set(xticks=[], yticks=[])
ax_arr[1].set_frame_on(False)

plt.savefig(FIG_PATH, bbox_inches='tight')
```
