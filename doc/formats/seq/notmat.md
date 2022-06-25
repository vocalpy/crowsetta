(notmat)=

# evsonganaly .not.mat format

Format of annotations saved by the evsonganaly GUI, written in Matlab.

The first work published with data collected using EvTAF and evsonganaly is in this paper:  
Tumer, Evren C., and Michael S. Brainard.  
"Performance variability enables adaptive plasticity of ‘crystallized’ adult birdsong."  
Nature 450.7173 (2007): 1240.  
<https://www.nature.com/articles/nature06390>  

This format is used for the dataset in this repository:
<https://figshare.com/articles/dataset/Bengalese_Finch_song_repository/4805749>

Internally, crowsetta loads this format using the 
Python tool [evfuncs](https://github.com/NickleDave/evfuncs).

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.notmat.NotMat`.
