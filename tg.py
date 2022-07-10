# author : Philippe Vo
# date   : Sat 09 Jul 2022 06:43:36 PM

# 3rd party imports
import musicbrainzngs
# user imports
from src.tools.music_db import MusicBrainzngsHelper

mh = MusicBrainzngsHelper()
mostLikelyArtistName, mostLikelyArtistID = mh.get_most_likely_artist("BTS")
mostLikelySong = mh.get_most_likely_song(mostLikelyArtistID, "Epipany")
