# author : Philippe Vo
# date   : Mon 04 Jul 2022 02:22:56 PM

# 3rd party imports
from musixmatch import Musixmatch
import lyricsgenius
import json
# user imports
from src.core.driver import Driver
from src.tools.lyrics import save_lyrics_into_mp3

songFilePath = input("song file [drag & drop file] : ").strip()
save_lyrics_into_mp3(songFilePath)

# token = "QW6XBQQ0SDzgs-4Fw6r97-ZE6vJguhpFX0SidG99ZA9sO4n5QiEs2InWwh6jokYV"
# genius = lyricsgenius.Genius(token)
# artist = genius.search_artist("Olivia Rodrigo", max_songs=0)
# song = artist.song("Wondering")
# print(song.lyrics)

# musixmatch = Musixmatch('03efeb192b853b8894a5bbb26b3454d0')
# lyrics = musixmatch.matcher_lyrics_get('Wondering', 'Olivia Rodrigo')
# print(lyrics)
# print(lyrics['message']['body']['lyrics']['lyrics_body'])

# driver = Driver()
# driver.run(songFilePath)
