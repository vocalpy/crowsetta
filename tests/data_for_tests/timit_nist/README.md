These are files from a version of TIMIT with audio files that end in .WAV, 
and annotation files that end in .PHN.

The .PHN files are the same as .phn files, it's just that the extension is all uppercase.

The .WAV files are actually a different format; specifically the NIST format.
This format can be parsed by `soundfile` but *not* by `wave` from the Python standard 
library or `scipy.io.wavefile`.

Presumably the `.WAV.wav` files are the NIST format converted to a more 
common .wav format.
I did verify for one file that both have the same sampling rate.
So literally I think they just removed the weird NIST header and 
converted to a standard .wav file.

Both file types are added here so tests can verify that:
- `phn2annot`  is case-insensitive, i.e., it parses .phn and .PHN files
- **and** `phn2annot` is case and "format" insensitive when parsing .wav 
  and .WAV files -- it's still able to figure out the sampling rate so 
  it can convert onset and offset times from sample number to seconds,
  regardless of whether it's a `.wav` or a `.WAV` file
 