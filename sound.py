import os
import random
cmd = 'omxplayer music/'


def play_random_sound():
    playlist = []
    for root, dirs, files in os.walk('./music'):
        playlist.append(files)
    random_number = int(len(playlist[0]) * random.random())
    filename = playlist[0][random_number]
    print('Now playing ' + filename)
    os.system(cmd + filename)


