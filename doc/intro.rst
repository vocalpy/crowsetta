===================================================
A Gentle Introduction to Working with ``crowsetta``
===================================================



Internally, `crowsetta` takes whatever format you give it for a pile of files, 
and turns that into a bunch of `Sequences` made up of `Segments`. 99.9% of
the time, the `Sequences` will be single audio files / song bouts, and the 
`Segments` will be syllables in those song bouts. Then, if you need it to, 
`crowsetta` can spit out your `Sequences` of `Segments` in a simple text file 
with a comma-separated value (csv) format. This file format was chosen because 
it is widely considered to be the most robust way to share data.

An example csv looks like this:
```
label, onset_s, offset_s, onset_Hz, offset_Hz, index, file
a, 1.01, 1.52, 32002, 33003, 1, bird_27_2018_11_28.wav
a, 2.01, 2.53, 64002, 65003, 2, bird_27_2018_11_28.wav
...
```

Now that you have that, you can load it into a `pandas` dataframe or an Excel 
spreadsheet or a SQL database, or whatever you want.


