# author : Philippe Vo
# date   : Mon 04 Jul 2022 02:22:56 PM

# 3rd party imports
from youtubesearchpython import VideosSearch
import youtube_dl
# user imports
from src.core.driver import Driver
from src.tools.lyrics import save_lyrics_into_mp3

videosSearch = VideosSearch('Wondering Olivia Rodrigo', limit = 3)

results = videosSearch.result()['result']
for result in results:
    print(result["title"], result["link"])

# to get the destination filename after downloading using youtube_dl
class FilenameCollectorPP(youtube_dl.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information
filename_collector = FilenameCollectorPP()

urlLink = result["link"]
ydl_opts = {
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

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.add_post_processor(filename_collector)
    ydl.download([urlLink])
    destinationFilePath = filename_collector.filenames[0]

save_lyrics_into_mp3(destinationFilePath)
