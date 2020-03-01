import os
import re
import urllib.request
from bs4 import BeautifulSoup

lyrics_folder = "lyrics/"
 
def get_lyrics(artist,song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
    
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()
        return lyrics
    except Exception as e:
        raise e

def get_all_lyrics():
    artist_name = "Tom petty and the heartbreakers"
    for song in listdir('data'):
        song_name = song[3:-4]
        try:
            lyrics = get_lyrics(artist_name, song_name)
            with open(lyrics_folder + song[:-4] + ".txt", "w") as f:
                f.writelines(lyrics) 
        except:
            print(song_name, " has error")


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    clean_new_lines = re.compile('\\n')
    # clean_backslashes = re.compile("\\")
    text = re.sub(clean, '', text) 
    text = re.sub(clean_new_lines, '', text)
    text = text.replace('\\', '')
    return text


def get_all_lyrics_from_file():
    lyric_song_list = []
    for lyric_file in os.listdir(lyrics_folder):
        song = lyric_file[:-4]
        with open(lyrics_folder + lyric_file, "r") as f:
            lyrics_txt = f.readlines()
            for idx, line in enumerate(lyrics_txt):
                line = remove_html_tags(line)
                line = line.strip()
                lyrics_txt[idx] = line
            lyric_song_list.append((song, lyrics_txt)) 
    return lyric_song_list


from os import listdir
if __name__ == "__main__":
    get_all_lyrics()
