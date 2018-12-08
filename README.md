# conbirt
A tool to ~~conbirt~~ convert different formats for annotating birdsong 
into a common, simple comma-separated value format.

The format looks like this:
```
label, onset_s, offset_s, onset_Hz, offset_Hz, index, file
a, 1.01, 1.52, 32002, 33003, 1, bird_27_2018_11_28.wav
a, 2.01, 2.53, 64002, 65003, 2, bird_27_2018_11_28.wav
...
```

`conbirt` is used by the `hybrid-vocal-classifier` and `songdeck` 
libraries.

You might find it useful in any situation where you want 
to share audio files of song and some associated annotations, 
but you don't want to require the user to install a large 
application in order to get access to the annotation files.

## installation
`pip install conbirt`

## usage


## citation
If you use `conbirt`, please cite the DOI:
