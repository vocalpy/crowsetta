(simple-seq)=

# simple-seq

One of two sequence-like formats that are meant to be general, 
and allow for working with a wide array of formats -- 
the other is {ref}`generic-seq`.

The `'simple-seq'` format can represent 
any {ref}`sequence-like <formats-seq-like>` format,   
that can be mapped to a sequence of segments, 
with each segment having an onset time, offset time, and label. 

A file in `'simple-seq'` format 
can be either a .csv or .txt file.
It should have 3 columns that represent
the onset and offset times in seconds
and the labels of the segments
in the annotated sequences.

The default is to assume
a comma-separated values file
with a header 'onset_s, offset_s, label',
but this can be modified
with keyword arguments to the `from_file` method 
of the class that represents the format.

This format also assumes that each annotation file
corresponds to one annotated source file,
i.e. a single audio or spectrogram file.
This is likely to be the case if you are using apps like Praat or Audacity. 
An example of such a format is the Audacity standard label track format, 
exported to .txt files, that you would get if you were to annotate with
region labels.

The annnotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.simple.SimpleSeq`.
