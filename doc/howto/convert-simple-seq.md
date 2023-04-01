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

+++ {"tags": []}

(howto-convert-to-simple-seq)=
# How to convert sequence-like annotations to the `'simple-seq'` format

A goal of crowsetta is to make it easier to work with annotations 
without knowing about the details of annotation formats. 
One situation where you will want to do this 
is when creating data sets for machine learning;
the software framework for building machine learning models 
should not need to know about all the different annotation formats, 
and as a user you should not be prevented from 
training models on your data 
just because you rely on a format not supported by the framework.

In this situation, you need a simplified format 
that retains only the information required to train 
machine learning models to perform the task.
crowsetta provides simplified representations 
of annotation formats that map directly to machine learning tasks, 
and makes it easy to convert your annotations 
in widely used formats to these simplified representations.

This vignette shows how to convert {ref}`sequence-like <formats-seq-like>` annotations 
to a simplified format that is useful for tasks 
such as building data sets for machine learning.
In this vignette, we write an example small Python script
to convert a set of annotations 
to the `'simple-seq'` format using the pandas library.
We then show that we are able to load the annotations 
with crowsetta after converting them.

## Background

### When would you want to do this

Imagine we are training a machine learning model 
on a supervised learning task 
where it is given an annotated file $x$ 
in some form, such as a spectrogram, 
and it learns to predict the annotations $y$.
Many software frameworks allow researchers to train such models 
and generate new productions 
given datasets $\mathcal{D}$ where each $d_i$ is a pair $(x_i, y_i)$.
It is typical to build $\mathcal{D}$ by pairing each of the samples $x$, 
say as an array saved to disk, 
with an annotation file $y$ in 
a lightweight, flat format such as a csv file. 

As stated above, 
when building such datasets, 
you usually want the most lightweight format possible 
for rapid loading from disk and/or storage in memory. 
You also want a generic annotation format 
that retains only the information required 
to train the model to perform the task, 
as stated above.

For example 
the [DAS library expects such a format](https://janclemenslab.org/das/technical/data_formats.html#annotations)
and the vak library similarly allows for 
[building datasets with a simple csv format](https://vak.readthedocs.io/en/latest/howto/howto_user_annot.html#method-1-converting-your-annotations-to-the-simple-seq-format)
(this vignette is adapted from that section of the vak docs).

### What types of annotation formats will this work with

The approach shown here will work for a wide array of annotation formats 
that crowsetta calls {ref}`sequence-like <formats-seq-like>`,
because they can all be represented as a sequence of segments, 
with each segment having an onset time, offset time, and label.

**The one assumption the `'simple-seq'` format makes is that you have one annotation file 
per file that is annotated, that is, 
one annotation file per audio file or per array file containing a spectrogram.**
This is likely to be the case if you are using apps like Praat or Audacity.
An example of such a format is the Audacity 
[standard label track format](https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format), 
exported to .txt files, that you would get if you were to annotate with  
[region labels](https://manual.audacityteam.org/man/label_tracks.html#type).
We use the Audacity format in this vignette.

### Downloading the example dataset

We download some examples of annotation files in the 
{ref}`Audacity LabelTrack format <aud-seq>`, 
from the dataset 
["Labeled songs of domestic canary M1-2016-spring (Serinus canaria)"](https://zenodo.org/record/6521932)
by Giraudon et al., 2021.

```{code-cell} ipython3
cd ..
```

```{code-cell} ipython3
!curl --no-progress-meter -L 'https://zenodo.org/record/6521932/files/M1-2016-spring_audacity_annotations.zip?download=1' -o './data/M1-2016-spring_audacity_annotations.zip'
```

```{code-cell} ipython3
import shutil
shutil.unpack_archive('./data/M1-2016-spring_audacity_annotations.zip', './data/giraudon-et-al-2021')
```

+++ {"tags": []}

First we explain what your dataset should look like.

### Explanation of when you can use the `'simple-seq'` format

Again, this first approach assumes that you have a separate 
annotation file for each file you have with a vocalization in it, 
either an audio file or an array file containing a spectrogram.
In other words, a directory of your data looks something like this:

```{code-cell} ipython3
ls ./data/giraudon-et-al-2021/audacity-annotations/ | head -10
```

Notice that each .wav audio file has 
a corresponding .txt file with annotations.
Each of the .txt files has columns 
that could be imported into a GUI application, e.g. Audacity.

Here's we use the `cat` command in the terminal 
to dump out the first few lines of the the first .audacity.txt file:

```{code-cell} ipython3
cat ./data/giraudon-et-al-2021/audacity-annotations/100_marron1_May_24_2016_62101389.audacity.txt | head -10
```

We can see that each row has an onset time, an offset time, and a text label.
The evenly-aligned columns tell us that they are separated by tabs 
(which you can also notice if you open the file in a text editor 
and move the cursor around).
Lastly we see that there is no *header*, that is, 
no first row with column names, such as "start time", "stop time", and "name".

What we want is to convert each .txt file to a comma-separated file
(a `.csv`) in the `'simple-seq'` format,
with a header that has the specific column names that crowsetta recognizes.
We can easily create such files with pandas. 
We will write a script to do so.
After running the script,  
we will have a `.csv` file for each .txt and .wav file in our directory, as shown:

```console
100_marron1_May_24_2016_62101389.wav
100_marron1_May_24_2016_62101389.audacity.txt
100_marron1_May_24_2016_62101389.audacity.csv
101_marron1_May_24_2016_64441045.wav
101_marron1_May_24_2016_64441045.audacity.txt
101_marron1_May_24_2016_64441045.audacity.csv
102_marron1_May_24_2016_69341205.wav
102_marron1_May_24_2016_69341205.audacity.txt
102_marron1_May_24_2016_69341205.audacity.csv
103_marron1_May_24_2016_73006746.wav
103_marron1_May_24_2016_73006746.audacity.txt
103_marron1_May_24_2016_73006746.audacity.csv
...
108_marron1_May_25_2016_25065494.wav
108_marron1_May_25_2016_25065494.audacity.txt
108_marron1_May_25_2016_25065494.audacity.csv
...
```

Notice also how the script (that we haven't shown you yet) 
names the new annotation files: 
we preserve the `.audacity` component of the filename.
Alternatively, we could have named the files by replacing 
the entire suffix `.audacity.txt` with the extension `.csv`, 
but one drawback of doing this 
is that we cannot have any other csv files 
with the exact same name in the directory, 
for example if we wanted to have an analysis file 
for each audio file. E.g., "108_marron1_May_25_2016_25065494.csv".
could contain features or measurements 
we extract from "108_marron1_May_25_2016_25065494.wav".
So by keeping the `.audacity` "extension" we allow multiple csv files 
with the same stem to sit side by side in the same directory.

+++

## Walkthrough
### Converting .txt files to the `'simple-seq'` format

Below is a short example script that loads the text files using pandas, 
and then adds the columns names needed before saving 
a new .csv file with the same values.

```{code-cell} ipython3
import pathlib

import pandas as pd

COLUMNS = ['onset_s', 'offset_s', 'label']


txt_files = sorted(pathlib.Path('./data/giraudon-et-al-2021/audacity-annotations').glob('*.txt'))

for txt_file in txt_files:
    txt_df = pd.read_csv(txt_file, sep='\t', header=None)  # sep='\t' because tab-separated
    txt_df.columns = COLUMNS
    # in next line, use `txt_file.name` to get the entire file name with audio extension
    # and then add the .csv extension to it, to follow naming convention
    csv_name = txt_file.parent / (txt_file.stem + '.csv')
    txt_df.to_csv(csv_name, index=False)  # we don't want an added index columns
```

### Using crowsetta to load the converted files in the `'simple-seq'` format

Finally we use crowsetta to load the files saved in `'simple-seq'` format, to show that we have successfully converted them.

```{code-cell} ipython3
csv_files = sorted(
    pathlib.Path('./data/giraudon-et-al-2021/audacity-annotations').glob(
        '*.audacity.csv'
    )
)
```

```{code-cell} ipython3
csv_files[:5]
```

```{code-cell} ipython3
import crowsetta

scribe = crowsetta.Transcriber(format='simple-seq')

simple_seqs = [
    scribe.from_file(csv_file) for csv_file in csv_files
]
```

We can print the first loaded annotation to confirm it looks like the csv we inspected above.

```{code-cell} ipython3
simple_seqs[0]
```

Yes, these are the same onset and offset times and segment labels we saw in the first csv file. If we were preparing a dataset for machine learning, as in the introduction above, we would now be ready to build that dataset.
