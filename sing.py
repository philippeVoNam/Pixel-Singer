# author : Philippe Vo
# date   : Thu 07 Jul 2022 08:59:39 AM

# 3rd party imports
import pylrc
import threading
import time
import eyed3
import yt_dlp
from pathlib import Path
from youtubesearchpython import VideosSearch
import os
import shutil
# user imports
from src.core.driver import Driver
from src.tools.lyrics import save_lyrics_into_mp3
from src.tools.setup_tools import get_user_choice
from src.tools.music_db import MusicBrainzngsHelper
from src.tools.general_tools import print_center

mh = MusicBrainzngsHelper()

# get artist and song title
artist = input("artist : ").strip()
title = input("song title : ").strip()
artist, mostLikelyArtistID = mh.get_most_likely_artist(artist)
# title = mh.get_most_likely_song(mostLikelyArtistID, title) # FIXME : the time to search is still too long ...
songSearch = "{} - {}".format(title, artist)
videosSearch = VideosSearch(songSearch, limit = 5)

results = videosSearch.result()['result']
resultsTitle = []
for result in results:
    resultsTitle.append(result["title"])

# get song mp3 file
idxChoose = get_user_choice(resultsTitle, "choose which link : ")
urlLink = results[idxChoose]["link"]
outputFolder = "output"
mp3FilePath = str(Path(outputFolder) / "{}-{}.mp3".format(title, artist))
ydl_opts = {
    'outtmpl': mp3FilePath,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }
    ,{
        'key': 'FFmpegMetadata'
    }
    ],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([urlLink])

# save lyrics
save_lyrics_into_mp3(artist, title, mp3FilePath)

# get lrc and mp3 file
with open(mp3FilePath, "r") as f:
    track = eyed3.load(mp3FilePath)
    tag = track.tag
    lrcString = tag.lyrics[0].text

# parse lrc file
subs = pylrc.parse(lrcString)
title = subs.title
artist = subs.artist
numLines = len(subs)

# play song
driver = Driver()
t = threading.Thread(target=driver.run,args=(mp3FilePath,))
t.start()

# clear console
os.system('cls' if os.name=='nt' else 'clear')

# setup to print in the center
columns = shutil.get_terminal_size().columns

print_center("Playing {} by {}".format(title, artist), columns)
print_center("---", columns)

# show lyrics loop
line = 0
startTime = time.time()
printNextLine = False
while True:
    elapsedTime = time.time() - startTime
    if elapsedTime > subs[line].time:
        print_center(subs[line].text.rstrip(), columns)
        line = line + 1
