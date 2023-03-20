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
execution:
  timeout: 120
---

(tutorial)=

# Tutorial

This tutorial introduces users to crowsetta.

## Finding out what annotation formats are built in to crowsetta

The first thing we need to do to work with any Python library is import
it.

```{code-cell} ipython3
import crowsetta
```

Now we can use the `crowsetta.formats.as_list()` function to find out what formats are
built in to Crowsetta.

```{code-cell} ipython3
crowsetta.formats.as_list()
```

## Getting some example data to work with

Since crowsetta is a tool to working with annotations of
vocalizations, we need some audio files containing vocalizations that
are annotated.

We download some examples of annotation files in the 
{ref}`Audacity LabelTrack format <aud-seq>`, 
from the dataset 
["Labeled songs of domestic canary M1-2016-spring (Serinus canaria)"](https://zenodo.org/record/6521932)
by Giraudon et al., 2021.

```{code-cell} ipython3
!curl --no-progress-meter -L 'https://zenodo.org/record/6521932/files/M1-2016-spring_audacity_annotations.zip?download=1' -o './data/M1-2016-spring_audacity_annotations.zip'
```

```{code-cell} ipython3
import shutil
shutil.unpack_archive('./data/M1-2016-spring_audacity_annotations.zip', './data/giraudon-et-al-2021')
```

We use `pathlib` from the Python standard library to 
get a list of those files.

```{code-cell} ipython3
import pathlib
audseq_paths = sorted(pathlib.Path('./data/giraudon-et-al-2021/audacity-annotations').glob('*.txt'))

print(f'There are {len(audseq_paths)} Audacity LabelTrack .txt files')
first_five = "\n".join([str(path) for path in audseq_paths[:5]])
print(f'The first five are:\n{first_five}')
```

## Using the `Transcriber` to load annotation files

Now we want to use crowsetta to load the annotations from files.

First we get all the annotation files in some variable.
(We have already done this using `pathlib.Path.glob` above.)

Now we use `crowsetta.Transcriber` to load them.
The `Transcriber` is a Python `class`, and we want to create a new
instance of that class. You don’t have to understand what that
means, but you do have to know that before you can do anything with a
`Transcriber`, you have to call the class, as if it were a function,
and assign it to some variable, like this:

```{code-cell} ipython3
scribe = crowsetta.Transcriber(format='aud-seq')
print("scribe is an instance of a", type(scribe))
```

Now we have a `scribe` with methods that we can use on our
annotation files (methods are functions that “belong” to a class). 
We use the `from_file` method of the `Transcriber` to load the annotations.

```{code-cell} ipython3
audseqs = []

for audseq_path in audseq_paths:
    audseqs.append(scribe.from_file(audseq_path))


print(f'There are {len(audseqs)} Audacity LabelTrack annotations')
print(f'The first one looks like:\n{audseqs[0]}')
```

## Using the `to_annot` method to convert annotations into data types we can work with in Python

Now that we have loaded the annotations, we want to get them into some
*data type* that makes it easier to get what we want out of the annotated files 
(in this case, audio files).
Just like Python has data types like a `list` or `dict` that make it
easy to work with data, crowsetta provides data types meant to 
work with many different formats.

For any format built into crowsetta, we can convert the annotations 
that we load into a generic `crowsetta.Annotation` (or a `list` of 
`Annotation`s, if a single annotation file contains annotations 
for multiple annotated audio files or spectrograms).

```{code-cell} ipython3
annots = []
for audseq in audseqs:
    annots.append(scribe.from_file(audseq_path).to_annot())
print(f'The first Annotation: {annots[0]}')
```

Depending on the format type, sequence-like 
or bounding box-lie, 
the `Annotation` will either have a `seq` attribute, 
short for "Sequence", or a `bbox` attribute, 
short for "Bounding box".
Since `'aud-seq'` is a sequence-like format, 
the `Annotation`s have a `seq` attribute:

```{code-cell} ipython3
print(
    f'seq for first Annotation: {annots[0].seq}'
)
```

**The two types of formats each have their own 
corresponding data type, `crowsetta.Sequence` and `crowsetta.BBox`** 
These are the data types that make it easier to work with your annotations. 
We work more with `Sequence`s below.

But first we mention a couple other features of `Annotation`s. 
When we convert the annotation to a generic `crowsetta.Annotation`, 
we retain the path to the original annotation file, 
in the attribute `annot_path`, 
and we optionally have the path to the file that it annotates, `notated_path`.

```{code-cell} ipython3
print(
    f'annot_path for first Annotation: {annots[0].annot_path}'
)
```

Notice that we can chain the methods `from_file` and `to_annot` 
to make loading the annotations and converting them 
to generic `crowsetta.Annotation`s into a one-liner:

```{code-cell} ipython3
annots = []
for audseq_path in audseq_paths:
    annots.append(scribe.from_file(audseq_path).to_annot())
```

We didn't do this above, just because we wanted to introduce the methods one-by-one.

+++

### Working with `Sequence`s

As we said, 
what we really want is some data types 
that make it easier to work with our annotations, 
and that help us write clean, readable code.

The {ref}`Audacity .txt <aud-seq>` format 
we are using in this tutorial above is one of what 
crowsetta calls a "sequence-like" format, 
as stated above.
What this means is that we can convert our 
each one of our `'aud-seq'` annotations to 
a `Sequence`. 
Each `Sequence` consists of some number of `Segment`s, i.e., a
part of the sequence defined by an `onset` and `offset` that has a
`label` associated with it.
These `Sequence`s and `Segment`s are what specifically helps  
us write clean code, as we'll see below.
(Bounding box-like annotation formats similarly give us generic 
`crowsetta.BBox`s that we can use to write code.)

Since we have already created the `crowsetta.Annotation`s, 
we can make a list of `crowsetta.Sequence`s from them 
by just grabbing the `Sequence` of each `Annotation`.

```{code-cell} ipython3
seqs = []
for annot in annots:
    seqs.append(annot.seq)
```

Notice again that we could have done this as a one-liner, 
using the `to_seq` method to load each file into a `Sequence`.
(but we didn't, because we wanted to explain the different methods to you):

```{code-cell} ipython3
seqs = []
for audseq_path in audseq_paths:
    seqs.append(scribe.from_file(audseq_path).to_seq())
```

Each sequence-like format has a `to_seq` method, 
and each bounding box-like format has a `to_bbox` method. 
When you call `to_annot`, that method actually calls `to_seq` 
or `to_bbox` when creating the `crowsetta.Annotation`s. 
But if you just need those data types, without the metadata 
provided by an `Annotation`, 
you can get them directly by calling the method yourselves.

For each annotation file, we should now have a `Sequence`.

```{code-cell} ipython3
print("Number of annotation files: ", len(audseq_paths))
print("Number of Sequences: ", len(seqs))
if len(audseq_paths) == len(seqs):
    print("The number of annotation files is equal to number of sequences.")
```

```{code-cell} ipython3
print("first element of seqs: ", seqs[0])
print("\nFirst two Segments of first Sequence:")
for seg in seqs[0].segments[0:2]: print(seg)
```

## **Using** crowsetta **data types to write clean code**

Now that we have a `list` of `Sequence`s, we can `iterate`
(loop) through it to get at our  data in a clean, Pythonic way.

Let's say we're interested in 
the number of occurrences of each class in our dataset, 
in this case, different phrases of the canary's song 
as well as some other sounds, like calls.
We also want to inspect the distribution of durations 
of each of these classes.

To achieve this, we will create a `pandas.Dataframe` 
and then plot distributions of the data in that `Dataframe` with `seaborn`.

+++

We loop over all the `Sequence`s, and then in an inner
loop, we’ll iterate through all the `Segment`s in each
`Sequence`, grabbing the `label` property from the `Segment` 
so we know what class it is, 
and computing the duration by subtracting 
the onset time from the offset time.

```{code-cell} ipython3
import pandas as pd

records = []

for sequence in seqs:
    for segment in sequence.segments:
        records.append(
            {
                'label': segment.label,
                'duration': segment.offset_s - segment.onset_s
            }
        )

df = pd.DataFrame.from_records(records)
from IPython.display import display
display(df.head(10))
```

(There are more concise ways to do that, but doing it the way we did let
us clearly see iterating through the `Segment`s and
`Sequence`s.)

```{code-cell} ipython3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("paper")
```

First we plot the counts for each phrase type. We notice there are many more silent periods ("SIL") and observe some smaller differences between the phrases themselves.

```{code-cell} ipython3
fig, ax = plt.subplots(figsize=(10,3), dpi=300)
sns.countplot(data=df, x='label', ax=ax)
ax.set_xticklabels(ax.get_xticklabels(),rotation = -45);
```

Now let's find the three most frequently-occurring phrases and examine the distributions of their durations. We ignore the silent periods.

```{code-cell} ipython3
df = df[df['label'] != 'SIL']  # remove silent periods
counts = df['label'].value_counts()  # get the counts of the labels
most_frequent = counts[:3].index.values.tolist()  # find the top 3 most frequent
df = df[df['label'].isin(most_frequent)]  # keep those top 3 most frequent in the original DataFrame
```

```{code-cell} ipython3
sns.set(font_scale=2)
sns.displot(data=df, x='duration', col='label', hue='label', col_wrap=3)
```

We can see that each phrase has a roughly similar distribution of durations. We also notice that for each phrase type there's one bin containing many very short durations, that we may want to inspect more closely in our data, to better understand how they arise. (This is one example of why it's always a good idea to visualize the descriptive statistics of any dataset you work with.)

+++

Okay, now you’ve seen the basics of working with crowsetta. Get out
there and analyze some vocalizations!

```{code-cell} ipython3
:tags: [remove-cell]
shutil.rmtree('./data/giraudon-et-al-2021/audacity-annotations')
```
