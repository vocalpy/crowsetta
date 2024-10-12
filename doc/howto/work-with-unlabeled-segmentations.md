---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# How to work with unlabeled segmentations using `crowsetta.SimpleSeq`

+++

Sometimes, instead of animal sounds that have been annotated by a human, we have a "raw" segmentation of sounds, that is the output of some algorithm. For example, the signal processing-based algorithms in the [`vocalpy.segment`](https://vocalpy.readthedocs.io/en/latest/api/generated/vocalpy.segment.html) module.

crowsetta tries to make it easy for you to work with these segmentations, without needing all the machinery of VocalPy. The way to do this is with the `"simple-seq"` format, represented by the `crowsetta.SimpleSeq` class. This page gives you a brief example of how it's done.

+++

We use an example annotation file from [this dataset](https://datadryad.org/stash/dataset/doi:10.5061/dryad.g79cnp5ts) of mouse pup calls.

```{code-cell} ipython3
import crowsetta

go_path = crowsetta.example("GO", return_path=True)
print(go_path)
```

We can see that we have a csv file.  

If, instead of loading it with crowsetta, we first load the csv file with pandas, we can get an idea of what it looks like.

```{code-cell} ipython3
import pandas as pd

df = pd.read_csv(go_path)
df.head()
```

Notice that we have the start and stop times of the segments, in seconds. We also have a column with the source file for the segmentation, and the duration of the segment, neither of which we need for our current purposes. What we *don't* have are labels for the segments -- something that crowsetta typically expects.

+++

Let's see what we get if we load this example directly (instead of setting `return_path=True` to get the path to the annotation file as we did above).

```{code-cell} ipython3
go = crowsetta.example("GO")
print(go)
```

Hmm, so we can see that we have the same start and stop times from above, but they are now called `onsets_s` and `offsets_s`. And somehow we suddenly have `labels` for the segments, but it looks like they are all dashes (`"-"`). Notice that the `"source_file"` and `"duration"` columns have disappeared.

How did that happen?

Notice also that the annotation format is `SimpleSeq`, as stated at the top of this page. If we try to make an instance of `crowsetta.SimpleSeq` ourselves, though, using the `from_file` method, we will get an error.

```{code-cell} ipython3
crowsetta.SimpleSeq.from_file(go_path)
```

What crowsetta is telling us with is that the columns in the csv file don't have the expected names.

The secret is to use two arguments to the `from_file` method of the `crowsetta.SimpleSeq` class: `columns_map` and `default_label`, which is what the `crowsetta.example` function is doing under the hood.

```{code-cell} ipython3
crowsetta.SimpleSeq.from_file(
    go_path,
    columns_map={"start_seconds": "onset_s", "stop_seconds": "offset_s"},
    default_label="x",
)
```

What's happening here is that the `crowsetta.SimpleSeq` class loads the csv file into a `pandas.DataFrame`, just as we did above, and then uses `columns_map` to rename the columns `start_seconds` and `stop_seconds` to the names that the class expects, `onset_s` and `offset_s`. (These columns become attributes of an instance of the class called `onsets_s`, where `onsets` is pluralized, and `offsets_s`, also pluralized.) The other columns (`"source_file"` and `"duration"`) are not used.

You can also see that we got default labels that are all `"x"`s this time. That's because the *default value* for `default_label` is `"-"`, but as we're showing here, you can change it to something else as suits your needs.

Hopefully this makes it easier for you to work with different datasets!
