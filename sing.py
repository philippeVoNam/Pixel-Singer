# author : Philippe Vo
# date   : Thu 07 Jul 2022 08:59:39 AM

# 3rd party imports
import pylrc
import threading
import time
import eyed3
# user imports
from src.core.driver import Driver

# get lrc and mp3 file
mp3FilePath = input("mp3 file : ").strip()
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
