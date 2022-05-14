from typing import final
import urllib.request
import re

def getSongId(songName):

    songName = ''.join(e for e in songName if e.isalnum())
    final_query = songName + "+song+cover"

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query={}'.format(final_query))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return video_ids[0]


# print(getSongId("I'm Yours"))