(textgrid)=

# Praat .TextGrid files

Annotation format saved by the [Praat](https://www.fon.hum.uva.nl/praat/) application. 
More details about annotating with Praat can be found here:
<https://www.fon.hum.uva.nl/praat/manual/Intro_7__Annotation.html>
The specification for TextGrid objects is here: 
<https://www.fon.hum.uva.nl/praat/manual/TextGrid.html>

Internally, `crowsetta` uses the Python tool `textgrid`
(<https://github.com/kylebgorman/textgrid>) to load .TextGrid files. 
A version is distributed with `crowsetta` 
under [MIT license](https://github.com/kylebgorman/textgrid/blob/master/LICENSE).

The annotations can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.textgrid.TextGrid`.
