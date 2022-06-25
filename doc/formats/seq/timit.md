(timit)=

# the TIMIT dataset

Annotations from transcription files in the 
DARPA TIMIT Acoustic-Phonetic Continuous Speech Corpus (TIMIT).
See the README for the dataset here in the U. Penn Catalog:  
<https://catalog.ldc.upenn.edu/docs/LDC93S1/timit.readme.html>

The formats that can be loaded with crowsetta are those used 
by the .wrd and .phn transcription files, 
where each segment is specified in terms of 
the sample number in the audio files where it begins, 
the sample where it ends,
and a text label. 
Columns are in that order, and there is no header.
For more detail, see section 5 of the TIMIT README, 
"File Types".

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.timit.Timit`.
