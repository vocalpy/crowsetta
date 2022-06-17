(birdsong-recognition-dataset)=

# BirdsongRecognition dataset

A {ref}`sequence-like <formats-seq-like>` annotation format 
used with the following dataset:  
Koumura, T. (2016). BirdsongRecognition (Version 1). figshare.  
<https://doi.org/10.6084/m9.figshare.3470165.v1>  
<https://figshare.com/articles/BirdsongRecognition/3470165>  

as used in this paper:  
Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188  
<https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0159188>  

The annotation format is schematized in 
[this XML schema file](https://github.com/NickleDave/birdsong-recognition-dataset/blob/main/doc/xsd/AnnotationSchema.xsd),
adapted [from the original](https://github.com/cycentum/birdsong-recognition/blob/master/xsd/AnnotationSchema.xsd) 
under the [GNU license](https://github.com/cycentum/birdsong-recognition/blob/master/LICENSE)
(file is unchanged except for formatting for readability).

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.birdsongrec.BirdsongRec`.
