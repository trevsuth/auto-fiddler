from music21 import converter, stream

# Single Tune
file = "./downloaded_files/01_Butterfly.abc"
abcScore = converter.parse(file, format="abc")
print(type(abcScore))
print(isinstance(abcScore, stream.Opus))
print(isinstance(abcScore, stream.Score))


# many tunes
file = "./downloaded_files/_Petrie_1st_Coll.txt"
abcScore = converter.parse(file, format="abc")
print(type(abcScore))
print(isinstance(abcScore, stream.Opus))
print(isinstance(abcScore, stream.Score))

# abcScore.show('text')
