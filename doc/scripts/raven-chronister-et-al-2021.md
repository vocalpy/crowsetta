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
import shutil

import soundfile

import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pyprojroot

import crowsetta
```

```{code-cell} ipython3
def plot_spect(S_db, sr, 
               hop_length=16, win_length=1024, 
               figsize=(10, 4), dpi=300,
               x_coords=None, cmap='magma',
               ylim=None, tlim=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, win_length=win_length, 
                                   x_coords=x_coords, y_axis='linear', x_axis='time', 
                                   ax=ax, cmap=cmap)

    if tlim:
        ax.set_xlim(tlim)
    if ylim:
        ax.set_ylim(ylim)
```

```{code-cell} ipython3
def plot_bboxes(bboxes, tlim, ax, colormap):
    for bbox in bboxes:
        if bbox.onset > tlim[0] and bbox.offset < tlim[1]:
            xy = (bbox.onset, bbox.low_freq)
            width = bbox.offset - bbox.onset
            height = bbox.high_freq - bbox.low_freq
            edgecolor = colormap[bbox.label]
            rect = Rectangle(xy, width, height, linewidth=2, 
                             edgecolor=edgecolor, facecolor='none', label=bbox.label)
            ax.add_patch(rect)

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(),
              facecolor='gainsboro',
              bbox_to_anchor=(1.01,0.5), loc="center left")
```

```{code-cell} ipython3
SCRIPTS_ROOT = pyprojroot.here() / 'doc/scripts'

WAV_PATH = SCRIPTS_ROOT / 'audio' / 'Recording_1_Segment_07-snippet.wav'
RAVEN_PATH = SCRIPTS_ROOT / 'annot' / 'Recording_1_Segment_07.Table.1.selections.txt'

STATIC_ROOT = pyprojroot.here() / 'doc/_static'
FIG_PATH = STATIC_ROOT / 'example-raven-for-index.png'
```

```{code-cell} ipython3
raven = crowsetta.formats.by_name('raven').from_file(RAVEN_PATH, annot_col='Species')
bboxes = raven.to_bbox()

# first four are the ones that appear in snippet so we manually pick colors for them.
# others are just to avoid errors upon dict lookup
LBL_COLOR_MAP = {
    'NOCA': 'c',
    'BCCH': 'y',
    'EATO': 'r',
    'WOTH': 'w',
    'BAWW': 'b',
    'OVEN': 'm,',
    'TUTI': 'g',
    'WITU': 'k',
 }
```

```{code-cell} ipython3
FS = 32000  # original file sampling rate
# we need original start and stop times,
# so we can show them on x-axis, and so 
# we know what segment annotations to plot
TLIM_S_ORIGINAL = [0, 10]
TLIM_INDS = [int(t * FS) for t in TLIM_S_ORIGINAL]
assert TLIM_INDS == [0, 320000]
```

```{code-cell} ipython3
hop_length=16
win_length=1024

y, sr = librosa.load(WAV_PATH, sr=None)  # sr=None to use original sampling rate

D = librosa.stft(y, hop_length=hop_length, win_length=win_length)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
```

```{code-cell} ipython3
FONT_SIZE = 14

plt.rc('font', size=FONT_SIZE)
plt.rc('axes', labelsize=FONT_SIZE)
plt.rc('xtick', labelsize=FONT_SIZE)
plt.rc('ytick', labelsize=FONT_SIZE)
plt.rc('legend', fontsize=FONT_SIZE)

fig, ax = plt.subplots(figsize=(10, 4), dpi=300)

idx = np.array(range(0, S_db.shape[1]))
x_coords = librosa.frames_to_time(idx, sr=sr, hop_length=hop_length, n_fft=2048)

plot_spect(S_db, sr,
           hop_length=64, win_length=512,
           x_coords=x_coords, ylim=[1096, 6000], ax=ax)

plot_bboxes(bboxes, tlim=TLIM_S_ORIGINAL, ax=ax, colormap=LBL_COLOR_MAP)

plt.savefig(FIG_PATH, bbox_inches='tight')
```
