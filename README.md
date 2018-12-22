# crowsetta
A tool to ~~conbirt~~ work with any format for annotating birdsong.
**The goal of `crowsetta` is to make sure that your ability to work with a 
dataset does not depend on your ability to work with any given format for 
annotating that dataset. `crowsetta` does not to provide yet another format 
for annotating birdsong!** (I promise.) 

Internally, `crowsetta` takes whatever format you give it for a pile of files, 
and turns that into a bunch of `Sequences` made up of `Segments`. 99.99% of
the time, the `Sequences` will be single audio files / song bouts, and the 
`Segments` will be syllables in those song bouts. Then, if you need it to, 
`crowsetta` can spit out your `Sequences` of `Segments` in a simple text file 
with a comma-separated value (csv) format. This file format was chosen because 
it is widely considered to be the most robust way to share data.

So the csv file would look something like this:
```
label, onset_s, offset_s, onset_Hz, offset_Hz, index, file
a, 1.01, 1.52, 32002, 33003, 1, bird_27_2018_11_28.wav
a, 2.01, 2.53, 64002, 65003, 2, bird_27_2018_11_28.wav
...
```

Now that you have that, you can load it into a `pandas` dataframe or an Excel 
spreadsheet or a SQL database, or whatever you want.

`crowsetta` is used by the `hybrid-vocal-classifier` and `songdeck` 
libraries.

You might find it useful in any situation where you want 
to share audio files of song and some associated annotations, 
but you don't want to require the user to install a large 
application in order to work with the annotation files.

## installation
`pip install crowsetta`

## usage


## citation
If you use `crowsetta`, please cite the DOI:

## build status
[![Build Status](https://travis-ci.com/NickleDave/crowsetta.svg?branch=master)](https://travis-ci.com/NickleDave/crowsetta)