# author : Philippe Vo
# date   : Sat 09 Jul 2022 06:43:36 PM

# 3rd party imports
import musicbrainzngs
import threading
import time
# user imports
from src.tools.general_tools import string_similar, get_most_likely_str

class MusicBrainzngsHelper:
    def __init__(self):
        musicbrainzngs.set_useragent("default", "0", "http://example.com/music")

    def get_most_likely_artist(self, searchArtist):
        result = musicbrainzngs.search_artists(artist=searchArtist, type="group", country="GB")

        artistNames = []
        artists = result['artist-list']
        for artist in artists:
            artistName = artist["name"]
            artistNames.append(artistName)

        mostLikelyIdx = get_most_likely_str(searchArtist, artistNames)
        mostLikelyArtistName = artists[mostLikelyIdx]["name"]
        mostLikelyArtistID = artists[mostLikelyIdx]["id"]

        return mostLikelyArtistName, mostLikelyArtistID

    def get_recordings(self, artistID, recordingsList, limit, offset):
        result = musicbrainzngs.browse_recordings(artistID, limit = limit, offset = offset)
        recordings = result['recording-list']
        for recording in recordings:
            recordingsList.append(recording["title"])

    def get_most_likely_song(self, searchArtistID, searchSong):
        recordings = []
        pages = 3
        limitNum = 100
        for i in range(pages):
            self.get_recordings(searchArtistID, recordings, limitNum, i * limitNum)

        mostLikelyIdx = get_most_likely_str(searchSong, recordings)
        mostLikelySong = recordings[mostLikelyIdx]

        return mostLikelySong
