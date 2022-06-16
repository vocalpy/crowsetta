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
---

(howto-convert-to-generic-seq)=
# How to convert any sequence-like format to `'generic-seq'`

The `'generic-seq'` format is 
meant to be a generic sequence-like format
(as suggested by its name) 
that all other formats can be converted to.
As explained on its  
{ref}`documentation <generic-seq>` page,
a set of `generic-seq` annotations is 
literally a set of `crowsetta.Annotation` instances 
where each `Annotation` has a `Sequence`.

Since all sequence-like formats have a `to_annot` 
method, they can all be converted to `'generic-seq'`.
In turn, this means that any sequence-like format 
can be converted to a flat .csv file, 
by creating a `'generic-seq'` instance with the 
`Annotations` produced by calling `to_annot` 
and then calling the `to_file` method of 
the `'generic-seq'` instance.
Saving annotations to a single flat .csv file 
may make it easier to share and 
work with them  
(e.g., using the {ref}`pandas <https://pandas.pydata.org/>` library).

## Converting a sequence-like format with multiple annotations per file

Some formats contain multiple annotations per file, 
and the `to_annot` method of the corresponding class 
will return multiple `crowsetta.Annotation` instances. 
To convert this format to `'generic-seq'`, 
just pass in those `Annotation`s when 
creating an instance of `'generic-seq'`

```{code-cell} ipython3
import crowsetta

example = crowsetta.data.get('birdsong-recognition-dataset')
birdsongrec = crowsetta.formats.seq.BirdsongRec.from_file(example.annot_path)
annots = birdsongrec.to_annot()
print(
    f"Number of annotation instances in example 'birdsong-recognition-dataset' file: {len(annots)}"
) 

# pass in annots when creating generic-seq instance
generic = crowsetta.formats.seq.GenericSeq(annots=annots)
print(
    f"Converted to 'generic-seq':\n{generic}"
)
```

## Converting a sequence-like format with a single annotation file per annotated file

When the convention for a format 
is to have a one-to-one mapping 
from annotated file to annotation file, 
and we want to put multiple such annotations 
into a single generic sequence file,
we need to go through an additional step.
That step consists of collecting all the annotations into a list.

For this example, 
we use the same dataset we used in the {ref}`tutorial`, 
["Labeled songs of domestic canary M1-2016-spring (Serinus canaria)"](https://zenodo.org/record/6521932)
by Giraudon et al., 2021, 
annotated with {ref}`Audacity Labeltrack {aud-txt}` files.

```{code-cell} ipython3
!curl --no-progress-meter -L 'https://zenodo.org/record/6521932/files/M1-2016-spring_audacity_annotations.zip?download=1' -o './data/M1-2016-spring_audacity_annotations.zip'
```

```{code-cell} ipython3
import shutil
shutil.unpack_archive('./data/M1-2016-spring_audacity_annotations.zip', './data/')
```

```{code-cell} ipython3
import pathlib
import crowsetta

audtxt_paths = sorted(pathlib.Path('./data/audacity-annotations').glob('*.txt'))
# we make the list of ``Annotation``s "by hand" instead of getting it from a `to_annot` call
annots = []
for audtxt_path in audtxt_paths:
    annots.append(
        crowsetta.formats.seq.AudTxt.from_file(audtxt_path).to_annot
    )

print(
    f"Number of annotation instances from Giraudon et al. 2021: {len(annots}"
) 

# pass in annots when creating generic-seq instance
generic = crowsetta.formats.seq.GenericSeq(annots=annots)
print(
    f"Converted to 'generic-seq':\n{generic}"
)
```
