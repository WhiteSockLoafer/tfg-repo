import lyricsgenius
from .credentials import ACCESS_TOKEN

genius = lyricsgenius.Genius(ACCESS_TOKEN)
artist = genius.search_artist("Kendrick Lamar", max_songs=5)
song = artist.song("HUMBLE.")
print(song.lyrics)