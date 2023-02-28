(aud-seq)=

# Audacity Label Track .txt files

The `'aud-seq'` format describes 
[Audacity label tracks](https://manual.audacityteam.org/man/label_tracks.html) 
that have been exported to the 
[standard format](https://manual.audacityteam.org/man/importing_and_exporting_labels.html#Standard_.28default.29_format).

As described on the "standard format" page above:

> The standard structure to display a label denoting its Timeline position and any text it contains is as below.
>
> ```text
> 2.150000  →  2.150000  →  point label at 2.15 seconds
> 3.400000  →  6.100000  →  region label from 3.4 to 6.1 seconds
> ```
>
> In the example above, the first column has the start time in seconds, 
> the second column has the end time, and the third column if present shows the text of the label. 
> Start time and end time are identical for a point label. Values are separated by tab characters 
> (which will often appear as an arrow in text editors, as shown above). 

Annotations in this format can be loaded with the following class: 
{py:class}`crowsetta.formats.seq.audseq.AudSeq`.