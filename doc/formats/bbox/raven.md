(raven)=

# Raven .txt files

Annotation format for the [Raven](https://ravensoundsoftware.com/software/raven-pro/) 
application that uses {ref}`bounding boxes <formats-bbox-like>`.
Bounding boxes in this format are determined by a start time (s), end time (s), 
low freq. (Hz), and high freq (Hz), 
as specified in Chapter 6 of the 
[user's manual](https://ravensoundsoftware.com/wp-content/uploads/2017/11/Raven14UsersManual.pdf).
Tables of bounding box selections can be exported to .txt files 
as described in the on-line knowledge base
[here](https://ravensoundsoftware.com/knowledge-base/save-all-selections-in-current-tables/).

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.bbox.raven.Raven`.
