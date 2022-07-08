from youtubesearchpython import VideosSearch
import youtube_dl

videosSearch = VideosSearch('Wondering Olivia Rodrigo', limit = 2)

results = videosSearch.result()['result']
for result in results:
    print(result["title"], result["link"])

urlLink = result["link"]
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([urlLink])
