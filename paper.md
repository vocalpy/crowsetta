---
title: 'Crowsetta: A Python tool to work with any format for annotating animal vocalizations and bioacoustics data.'
tags:
  - animal acoustic communication
  - bioacoustics
  - Python
authors:
  - name: David Nicholson
    orcid: 0000-0002-4261-4719
    corresponding: true
    affiliation: 1
affiliations:
  - name: Independent Research, USA
    index: 1
date: 07 Mar 2023
bibliography: paper.bib
---

# Summary

Studying how animals communicate with sound allows researchers to answer 
a wide range of questions, from "What species of birds live in this area?", 
to "How do mice mothers protect their young?". 
Some animals learn their vocalizations, and by studying the vocal behavior 
of these animals we can investigate questions like "How did speech evolve?".
Answering these questions require computational methods and big team science 
across many disciplines, 
such as ecology, ethology, bioacoustics, psychology, neuroscience, linguistics, and genomics.

Analyses of animal acoustic communication often require annotating 
the sounds animals make. 
To annotate animal sounds, researchers typically use graphical user interfaces (GUIs),
that enable them to annotate audio and/or spectrograms.
Such annotations usually include the times when sound events start and stop, and labels that 
assign each sound to some set of classes chosen by the annotator.
GUI applications save the annotations in many different file formats.
This Python package, crowsetta, can parse the most widely used formats,
and it provides software abstractions 
that make it easy to extend the library to parse new formats. 
In this way, crowsetta allows researchers 
to work with data annotated in a wider variety of formats. 
Additionally, crowsetta helps users convert annotations to simple file formats,
such as csv files, that do not require detailed knowledge of the annotation format itself.
This facilitates loading the annotations with widely used libraries 
for data analysis (e.g., Pandas in Python), 
and also promotes sharing data.
Overall, crowsetta supports the interdisciplinary collaboration 
required for the study of animal acoustic communication.

# Statement of need

Studying how animals communicate with sound 
allows researchers to answer a wide range of questions.
For example: 
"What is the language faculty, and how did it evolve?" [@hauser_faculty_2002], 
and "What is the basis of learned vocalizations in animals?" [@wirthlin_modular_2019]. 
Answering these questions will require big team science 
and true interdisciplinary collaborations [@hauser_faculty_2002; @wirthlin_modular_2019].
The methods used to answer these questions 
are becoming ever more computational and data driven.
As one example of such methods, deep learning models
have recently proliferated in the field of bioacoustics [@stowell_computational_2022] 
and adjacent fields like animal behavior [@berman_measuring_2018; @pereira_quantifying_2020], 
specifically studies of vocal behavior [@sainburg_toward_2021]. 
These models have also become common in the field of neuroscience [@cohen_recent_2022], 
and more specifically in studies of the neural bases of vocal communication
[@coffey_deepsqueak_2019; @cohen_automated_2022; @goffinet_low-dimensional_2021; @sainburg_finding_2020; @steinfath_fast_2021].
The performance of these data-driven deep learning models depends crucially on annotated data.
High-quality annotations from humans 
are needed to train supervised learning models to predict annotations
[@coffey_deepsqueak_2019; @cohen_automated_2022; @steinfath_fast_2021], 
or to provide inputs to unsupervised models that perform dimensionality reduction 
and compute measures of similarity [@goffinet_low-dimensional_2021; @sainburg_finding_2020].
In spite of this clear-cut need for high quality, easily accessible 
human annotations of animal acoustic communication data, 
it is surprisingly difficult to work with these annotations in code.
Ironically, researchers studying animal acoustic communication 
face challenges when communicating with each other.

This barrier arises in part because of the lack of a generalized schema 
for annotating audio datasets, which in turn results in a proliferation of 
annotation formats.
A standardized format for annotations would greatly facilitate interoperability, 
one of the guiding FAIR principles [@wilkinson_fair_2016]
There are some existing schema 
for bioacoustics datasets that include annotations 
[@roch_tethys_nodate; @baskauf_tdwgac_2022; @recalde_pykanto_nodate; @recalde_pykanto_2023; @fukuzawa_computational_2022] 
but there has been no broad effort at standardization.
Likewise, in animal behavior and neuroscience, 
specifically in areas that study acoustic communication,
there have been proposals for datasets structures, 
file formats, and databases schema, e.g. @dragly_experimental_2018, 
that would by necessity include annotations.
But again there has been little formalization across research groups 
and again, no wider effort to make these interoperable with audio annotations more generally.
The most direct work on standardization that I am aware of 
is the Json Annotated Music Specification (JAMS) [@humphrey_jams_2014; @mcfee_pump_nodate],
a standard for annotation in music information retrieval research.
One implementation of this standard 
has been provided in a Python library of the same name [@humphrey_jams_2014].
These issues were discussed at the first 
Audio Across Domains (AudioXd) conference (<https://kitzeslab.github.io/audioxd/>),
and a generalizable schema for audio annotation is being proposed 
(in preparation).
In the meantime, the lack of standardization 
creates a clear need for software tools that provide a sort of interoperability layer.

Currently, there is little tooling available that 
makes it easy to convert between annotation formats, 
and to share annotations in widely used simple formats such as a csv file.
Many tools have been developed 
to work with specific formats, 
e.g., Praat Textgrid [@jadoul_introducing_2018-1; @buschmeier_textgridtools_nodate] 
or Raven selection tables saved as text files (in Python [@haupert_scikit-maadscikit-maad_2022], 
and in R [@araya-salas_rraven_2020]), 
but to the best of my knowledge there are no tools that 
focus specifically on interoperability of formats.
This lack of tooling stands in contrast to the clear-cut need for researchers to be able to 
collaborate across disciplines when working with annotated audio datasets.

Crowsetta addresses the clear need for a tool 
that allows for interoperability between the many existing annotation formats, 
and that makes it possible to flexibly access annotations within Python 
for development of downstream applications.
Crowsetta also meets the needs of researchers to easily share annotations and 
to use them within Python for imperative code, 
e.g., scientist-coder scripts used to fit statistical models or analyze behavior. 
To address these needs all these needs, 
the package has built-in support for many widely used formats such as 
Audacity [@audacity_team_audacity_2019] label tracks, 
Praat [@paul_boersma_praat_2021] TextGrid files, 
and Raven [@program_raven_2016; @charif_raven_2006] 
selection tables exported to text files.
The design of crowsetta also focuses on interoperability.
It allows researchers to convert annotations 
loaded into built-in formats 
to more generic formats: 
for example, a generic "sequence-like" format 
that can represent annotated sequences of speech and animal vocalizations.
This generic format can be saved as a csv file, making data easier to share 
and easier to work with through widely-used data analysis libraries 
like Pandas [@reback2020pandas; @mckinney-proc-scipy-2010], 
In this way crowsetta minimizes the need for specialized knowledge of tool-specific formats.
In sum, the package provides a Pythonic way to work with annotation formats 
for animal vocalizations and bioacoustics data.

Originally, crowsetta was developed for use with vak [@nicholson_vak_2022], 
a neural network framework for researchers studying animal acoustic communication.
Crowsetta made it possible to work with several annotation formats 
when using vak to benchmark a neural network architecture 
that automates annotation of birdsong, TweetyNet [@cohen_automated_2022; @cohen_tweetynet_2023].
Since then, crowsetta has been used 
in tandem with vak by several research groups 
in neuroscience [@goffinet_low-dimensional_2021;@mcgregor_shared_2022] 
and bioacoustics [@provost_impacts_2022].

# Acknowledgements

I would like to acknowledge support from Yarden Cohen 
for development of crowsetta as part of the VocalPy ecosystem.
I would also like to acknowledge 
contributions to crowsetta during the pyOpenSci review,
made by the two reviewers, 
Tessa Rhinehart and Sylain Haupert, 
as well as expert advice from Yannick Jadoul on support for TextGrid, 
with guidance of Chia Marmo as the editor.

# References
