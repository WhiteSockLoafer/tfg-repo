import lyricsgenius
from credentials import ACCESS_TOKEN

genius = lyricsgenius.Genius(ACCESS_TOKEN, timeout=15, retries=3)
genius.remove_section_headers = True
genius.skip_non_songs = False
genius.excluded_terms = ["(Remix)", "(Live)", "(Demo)", "(Instrumental)"]

artist = genius.search_artist("Tyler, the creator", get_full_info=False)

with open("lyrics.txt", 'a', encoding='utf-8') as f:
    for song in artist.songs:
        print(song.lyrics)
        f.write(song.lyrics)