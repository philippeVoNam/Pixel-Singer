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
from difflib import SequenceMatcher

def string_similar(strA, strB):
    return SequenceMatcher(None, strA.lower(), strB.lower()).ratio()

def lyricsify_find_song_lyrics(query):
    """
    Return song lyrics from Lyricsify.com for the first song found using the provided search string.
    If not found, return None.
    """
    # Search Lyricsify for the song using web scraping
    links = BeautifulSoup(
        requests.get(url="https://www.lyricsify.com/search?q=" +
                     query.replace(
                         " - ", "+").replace(" ", "+"),
                     headers={
                         "User-Agent": ""
                     }).text,
        "html.parser").find_all("a", class_="title")

    # check how similiar the link text is to the query (aka title and artist of the song)
    linkWithHighestSimiliarity = ""
    highestSimiliarScore = 0
    for link in links:
        similiarScore = string_similar(query, link.text)
        if similiarScore > highestSimiliarScore:
            highestSimiliarScore = similiarScore
            linkWithHighestSimiliarity = link

    # If not found, return None
    if linkWithHighestSimiliarity is None:
        return None
    # Scrape the song URL for the lyrics text
    song_html = BeautifulSoup(
        requests.get(url="https://www.lyricsify.com" + linkWithHighestSimiliarity.attrs['href'],
                     headers={
            "User-Agent": ""
        }).text,
        "html.parser")

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

    return query, audio_file

def save_lyrics_into_mp3(artist: str, title: str, mp3FilePath: str):
    try:
        # query, audio_file = form_query_for_mp3(mp3FilePath)
        query = "{} - {}".format(artist, title)
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
