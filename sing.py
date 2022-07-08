# author : Philippe Vo
# date   : Thu 07 Jul 2022 08:59:39 AM

# 3rd party imports
import pylrc
import threading
import time
import eyed3
import yt_dlp
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

# to get the destination filename after downloading using yt_dlp
class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information
filename_collector = FilenameCollectorPP()

idxChoose = get_user_choice(resultsTitle, "choose which link : ")
urlLink = results[idxChoose]["link"]
ydl_opts = {
    'format': 'worstaudio/worst',
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
    ydl.add_post_processor(filename_collector)
    ydl.download([urlLink])
    mp3FilePath = filename_collector.filenames[0]

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
print("Playing {} by {}".format(title, artist))

# show lyrics loop
line = 0
startTime = time.time()
printNextLine = False
while True:
    elapsedTime = time.time() - startTime
    if elapsedTime > subs[line+1].time:
        printNextLine = True
        line = line + 1

    else:
        printNextLine = False

    if printNextLine:
        print(subs[line].text.rstrip() + " " * (60 - len(subs[line].text)))
