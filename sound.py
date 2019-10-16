import os
import random
cmd = 'omxplayer music/'


def play_random_sound():
    playlist = []
    for root, dirs, files in os.walk('./music'):
        playlist.append(files)
    filename = playlist[0][int((len(playlist)+1) * random.random())]
    print('Now playing ' + filename)
    os.system(cmd + filename)


