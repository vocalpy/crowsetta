(formats-index)=

# Formats

(formats-seq-like)=

## Sequence-like

These formats can all be represented as a sequence of segments, 
with each segment having an onset time, offset time, and a label 
that assigns it to a specific class.

### widely-used

These are sequence-like formats for widely-used applications

- {ref}`Praat .TextGrid files <textgrid>`
- {ref}`Audacity label tracks <aud-txt>`

### general

These are formats that can represent a wide variety of sequence-like 
annotation formats.

- {ref}`simple-seq`
- {ref}`generic-seq`

### dataset- or tool-specific

These are formats for specific tools or datasets.
Many of them can be represented by `simple-seq` or `generic-seq` 
but are provided a separate format for convenience.

- {ref}`birdsong-recognition-dataset`
- {ref}`notmat`
- {ref}`timit`

(formats-bbox-like)=

##  Bounding Box-like

These formats can all be represented as a set of bounding boxes, 
where each box has four coordinates representing its corners, 
as well as a label that assigns it to a specific class.

### dataset- or tool-specific

- {ref}`raven`
