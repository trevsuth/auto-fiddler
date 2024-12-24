# Auto-fiddler - A Project to train play with LLMs and fiddle tunes

### Goals
1. Identify tunes with the same melody but different names
1. Identify tunes with the same title but different melodies
1. Identify tunes that are idential but in diffferent time signatures (i.e. quarter notes in 4/4 but eighth notes in 2/2)
1. Identify tunes associated with a specific lineiage (i.e Scottish, Irish, Cape Breton, etc.)
1. Identify tunes that are idnetical save key signature
1. Classify tunes into the types genres (i.e. Jigs, Strasthpeys, etc)
1. Recognize tonal center

### Modules
1. Download - f(x) for downloading files
    1. Downloads files besed on sites listed in YAML files
    1. Removes duplicate files as IDed from a SHA hash
1. Extract - f(x) for preprocessing downloaded files
    1. Remove tunes from books files
    1. Generate summary statistics based on data in the coprus
        1. Number of files
        1. Distribution of length in # of bars
        1. Distribution of key signatures
    1. Save each file into musicXML format
    1. Create a midi representation of each file
    1. Extract moteifs from tunes
1. Embed
    1. Create an embedding of the musicXML file
    1. Create an embedding of the midi file
1. Save
    1. Save created vectors into a vector store for retreval later