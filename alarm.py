from pygame import mixer
import glob
import numpy as np
import datetime
import time
import sys
start = datetime.datetime.now()
print("Alarm started at {}".format(start))
try:
    wavs = glob.glob("/media/pi/SHODAN/Music/*.wav")
    mp3s = glob.glob("/media/pi/SHODAN/Music/*.mp3")
    songs = np.array(wavs + mp3s)
    np.random.shuffle(songs)
    mixer.init()
    print("    Playing {} songs".format(len(songs)))
    for song in songs:
        print("    {}".format(song))
        mixer.music.load(song)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(2)
        now = datetime.datetime.now()
        dt = now - start
        if dt.seconds >= 1.5*3600:
            sys.exit()
except Exception as e:
    print(e)

