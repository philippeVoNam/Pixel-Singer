# forked code from https://github.com/ImranR98/AutoLyricize

# 3rd party imports
import sys
import urllib
import json
from bs4 import BeautifulSoup
import requests
import os
import re
import eyed3

def lyricsify_find_song_lyrics(query):
    """
    Return song lyrics from Lyricsify.com for the first song found using the provided search string.
    If not found, return None.
    """
    # Search Lyricsify for the song using web scraping
    link = BeautifulSoup(
        requests.get(url="https://www.lyricsify.com/search?q=" +
                     query.replace(
                         " - ", "+").replace(" ", "+"),
                     headers={
                         "User-Agent": ""
                     }).text,
        "html.parser").find("a", class_="title")
    # If not found, return None
    if link is None:
        return None
    # Scrape the song URL for the lyrics text
    song_html = BeautifulSoup(
        requests.get(url="https://www.lyricsify.com" + link.attrs['href'],
                     headers={
            "User-Agent": ""
        }).text,
        "html.parser")
    # If the artist or song name does not exist in the query, return None
    artist_title = song_html.find("h1").string[:-7]
    sep_ind = artist_title.find("-")
    artist = None if sep_ind < 0 else artist_title[0:sep_ind].strip()
    title = artist_title if sep_ind < 0 else artist_title[sep_ind + 1:].strip()
    query_lower = query.lower()
    if query_lower.find(title.lower()) < 0 or (sep_ind >= 0 and query_lower.find(artist.lower()) < 0):
        return None
    # Return the lyrics text
    return "".join(song_html.find("div", id="entry").strings)

def form_query_for_mp3(mp3FilePath: str):
    eyed3.log.setLevel("ERROR")
    audio_file = eyed3.load(mp3FilePath)
    if audio_file.tag is None:
        audio_file.initTag()
        temp_ind = mp3FilePath.find("-")
        if len(mp3FilePath) > 0 and temp_ind > 0 and not mp3FilePath.endswith("-"):
            audio_file.tag.artist = mp3FilePath[0:temp_ind]
            audio_file.tag.title = mp3FilePath[temp_ind+1:]
            print(" : Warning : Artist/Title inferred from mp3FilePath name : ")
        else:
            print(" : Failed : Artist/Title could not be found : ")
            return
    existing_lyrics = ""
    for lyric in audio_file.tag.lyrics:
        existing_lyrics += lyric.text
    if len(existing_lyrics.strip()) > 0:
        print(" : Warning : File already has lyrics - skipped : ")
        return

    query = re.sub(r" ?\([^)]+\)", "",
                   audio_file.tag.artist + " - " + audio_file.tag.title)

    return query

def save_lyrics_into_mp3(mp3FilePath: str):
    try:
        query = form_query_for_mp3(mp3FilePath)
        lyrics = lyricsify_find_song_lyrics(query)
    except Exception as e:
        print("error getting Lyricsify lyrics for {} ".format(mp3FilePath))
        raise e
    if lyrics is not None:
        audio_file = eyed3.load(mp3FilePath)
        audio_file.tag.lyrics.set(lyrics)
        audio_file.tag.save()
        print("saved lyrics into {}".format(mp3FilePath))
    else:
        print("failed saving lyrics into {}".format(mp3FilePath))
