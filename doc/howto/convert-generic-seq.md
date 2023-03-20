---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
execution:
  timeout: 120
---

(howto-convert-to-generic-seq)=
# How to convert any sequence-like format to `'generic-seq'`

A goal of crowsetta is to make it easier to share annotations 
for a dataset of animal vocalizations or other bioacoustics data.
One way to achieve this is to 
convert the annotations to a single flat csv file,
which is easy to share and work with, 
e.g., using the [pandas](https://pandas.pydata.org/) library.
For {ref}`sequence-like <formats-seq-like>` annotations, 
this can be done by converting them to the `'generic-seq'` format.

This how-to walks you through converting 
annotations to the `'generic-seq'` format and 
then saving those annotations as a csv file.
As suggested by its name,
it is meant to be a generic sequence-like format
that all other sequence-like formats can be converted to.

## Workflow

Here's the general workflow. We'll see a few different ways to achieve it below.
1. Load annotations in your format
2. Convert those to {class}`crowsetta.Annotation` instances
3. Make a {class}`crowsetta.formats.seq.GenericSeq <crowsetta.formats.seq.generic.GenericSeq>` 
   from those `Annotation`s.
4. Save to a csv file using the 
   {meth}`crowsetta.formats.seq.generic.GenericSeq.to_file  <crowsetta.formats.seq.generic.GenericSeq.to_file>` 
   method

This works because `crowsetta` represents a set of annotations in `generic-seq` format 
as a list of {class}`crowsetta.Annotation` instances 
where each `Annotation` has a {class}`crowsetta.Sequence`.
Since all sequence-like formats have a `to_annot` 
method, they can all be converted to `'generic-seq'`.
In turn, this means that any sequence-like format 
can be converted to a flat .csv file, 
by creating a `'generic-seq'` instance with the 
`Annotations` produced by calling `to_annot` 
and then calling the `to_file` method of 
the `'generic-seq'` instance.

## Converting a sequence-like format with a single annotation file per annotated file

The first example we show is for possibly the most common case, 
where each annotated file has a single annotation file.
This is likely to be the case if you are using apps like Praat or Audacity.
An example of such a format is the Audacity 
[standard label track format](https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format), 
exported to .txt files, that you would get if you were to annotate with  
[region labels](https://manual.audacityteam.org/man/label_tracks.html#type).
This format is represented by the 
{class}`crowsetta.formats.seq.AudSeq <crowsetta.formats.seq.audseq.AudSeq>` 
class in crowsetta.

As described above,
all you need to do is load your sequence-like annotations 
with crowsetta, 
and then call the `to_annot` method 
to convert them to a {class}`crowsetta.Annotation` instance.
When working with a format 
where there's one annotation file per annotated file, 
this *does* mean you need to load **each** file 
and convert it into a separate annotation instance.
(Below we'll see an example of a format 
where annotations for multiple files 
are contained in a single annotation file, 
and so we only need to call `to_annot` once 
after loading it to get a list of 
{class}`crowsetta.Annotation`s.)
For this first example, 
where we have multiple annotation files, 
we use a loop to load each one and convert it to a 
{class}`crowsetta.Annotation` instance.
 
We use the same dataset we used in the {ref}`tutorial` for this example, 
["Labeled songs of domestic canary M1-2016-spring (Serinus canaria)"](https://zenodo.org/record/6521932)
by Giraudon et al., 2021, 
annotated with {ref}`Audacity Labeltrack <aud-seq>` files.

```{code-cell} ipython3
cd ..
```

First we download and extract the dataset, if we haven't already.

```{code-cell} ipython3
!curl --no-progress-meter -L 'https://zenodo.org/record/6521932/files/M1-2016-spring_audacity_annotations.zip?download=1' -o './data/M1-2016-spring_audacity_annotations.zip'
```

```{code-cell} ipython3
import shutil
shutil.unpack_archive('./data/M1-2016-spring_audacity_annotations.zip', './data/giraudon-et-al-2021')
```


Now we load the annotation files.

```{code-cell} ipython3
import pathlib
import crowsetta

audseq_paths = sorted(pathlib.Path('./data/giraudon-et-al-2021/audacity-annotations').glob('*.txt'))
# we make the list of ``Annotation``s "by hand" instead of getting it from a `to_annot` call
annots = []
for audseq_path in audseq_paths:
    annots.append(
        crowsetta.formats.seq.AudSeq.from_file(audseq_path).to_annot()
    )

print(
    f"Number of annotation instances from dataset: {len(annots)}"
) 
```

We create a set of annotations in the generic sequence format, by making an instance of the `GenericSeq` class, passing in our list of `crowsetta.Annotation` instances.

```{code-cell} ipython3
# pass in annots when creating generic-seq instance
generic = crowsetta.formats.seq.GenericSeq(annots=annots)
print("Created 'generic-seq' from annotations")
df = generic.to_df()
print("First five rows of annotations (converted to pandas.DataFrame)")
df.head()
```

```{code-cell} ipython3
print("Last five rows of annotations (converted to pandas.DataFrame)")
df.tail()
```

## Converting a sequence-like format with multiple annotations per file

Some formats contain multiple annotations per file, 
and the `to_annot` method of the corresponding class 
will return multiple `crowsetta.Annotation` instances. 
To convert this format to `'generic-seq'`, 
just pass in those `Annotation`s when 
creating an instance of `'generic-seq'`.
We demonstrate that here with the format of the Birdsong-Recognition dataset, 
using sample data built into the `crowsetta` package.

```{code-cell} ipython3
:tags: [hide-cell]

import crowsetta

crowsetta.data.extract_data_files()
```

```{code-cell} ipython3
import crowsetta

example = crowsetta.data.get('birdsong-recognition-dataset')
birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(example.annot_path)
# we pass a fake samplerate to suppress a warning about not finding .wav files
annots = birdsongrec.to_annot(samplerate=32000)
print(
    f"Number of annotation instances in example 'birdsong-recognition-dataset' file: {len(annots)}"
) 

# pass in annots when creating generic-seq instance
generic = crowsetta.formats.seq.GenericSeq(annots=annots)
print("Created 'generic-seq' from annotations")
df = generic.to_df()
print("First five rows of annotations (converted to pandas.DataFrame)")
df.head()
```

```{code-cell} ipython3
print("Last five rows of annotations (converted to pandas.DataFrame)")
df.tail()
```

To save these as a csv file, you can either call the `pandas.DataFrame.to_csv` method directly, or you can equivalently call the `GenericSeq` method `to_csv`.

```{code-cell} ipython3
df.to_csv('./data/birdsong-rec-pandas.csv', index=False)

generic.to_file('./data/birdsong-rec-generic-seq.csv')
```

Now you have seen two different ways to create a `GenericSeq` instance from a set of annotations, and then save them to a csv file so anyone can work with them!
