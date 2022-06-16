(generic-seq)=

# generic-seq

A generic format,
that like {ref}`'simple-seq' <simple-seq>` is 
meant to be an abstraction of
any sequence-like format.
The key difference between this format 
and `'simple-seq'` is that a single file in 
`'generic-seq'` format can contain 
annotations for multiple files. 
This makes it possible to "translate" 
other sequence-like formats with 
multiple annotations per file 
to `'generic-seq'`
(see {ref}`howto-convert-to-generic-seq`. 
By extension, 
this format can be used to 
produce a single file with annotations 
even in cases where the format 
is one-annotation-file-per-annotated-file, 
which may be helpful for sharing data 
or analysis tasks.

The format consists of ``Annotation``s,
each with a ``Sequence`` made up
of ``Segment``s.
These data types can then be saved to a .csv file
(by calling `crowsetta.formats.seq.generic.GenericSeq.to_file`), 
In such a .csv file, 
each row corresponds to one `Segment`.
The `annot` and `seq` columns in the row 
indicate which `Sequence` the `Segment` belongs 
to in a given `Annotation`
(in the vast majority of cases, 
there is just one `Sequence` per `Annotation`).

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.generic.GenericSeq`.
