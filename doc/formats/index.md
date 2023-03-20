(formats-index)=

# Formats

This page documents the annotation formats built in to crowsetta. 
The purpose of this section is to provide more information about 
the formats themselves, including links, citations, 
and schema where possible.
At the bottom of the page for each format there is a link 
to the class that can load annotations in that format, 
as documented in the 
{ref}`formats section of the API documentation <api-formats>`.

(formats-seq-like)=
## Sequence-like

These formats can all be represented as a sequence of segments, 
with each segment having an onset time, offset time, and a label 
that assigns it to a specific class.

### widely-used

These are sequence-like formats for widely-used applications:

- {ref}`Praat .TextGrid files <textgrid>`
- {ref}`Audacity label tracks <aud-seq>`

### general

These are formats that can represent a wide variety of sequence-like 
annotation formats.

- {ref}`simple-seq`
- {ref}`generic-seq`

### dataset- or tool-specific

These are formats for specific tools or datasets.
Many of them can be represented by `simple-seq` or `generic-seq` 
but are provided as a separate format for convenience.

- {ref}`birdsong-recognition-dataset`
- {ref}`notmat`
- {ref}`timit`

(formats-bbox-like)=
##  Bounding Box-like

These formats can all be represented as a set of bounding boxes 
on a spectrogram, 
where each box is defined by start and stop time 
as well as a low and high frequency range, 
and a label that assigns the box to a specific class.

### dataset- or tool-specific

- {ref}`raven`
