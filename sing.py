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
# user imports
from src.core.driver import Driver
from src.tools.lyrics import save_lyrics_into_mp3
from src.tools.setup_tools import get_user_choice

title = input("title : ").strip()
artist = input("artist : ").strip()
songSearch = "{} - {}".format(title, artist)
videosSearch = VideosSearch(songSearch, limit = 3)

results = videosSearch.result()['result']
resultsTitle = []
for result in results:
    resultsTitle.append(result["title"])

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

save_lyrics_into_mp3(artist, title, mp3FilePath)

# # get lrc and mp3 file
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
print("Playing {} by {}".format(title, artist))

# show lyrics loop
line = 0
startTime = time.time()
printNextLine = False
while True:
    elapsedTime = time.time() - startTime
    if elapsedTime > subs[line].time:
        print(subs[line].text.rstrip() + " " * (60 - len(subs[line].text)))
        line = line + 1
