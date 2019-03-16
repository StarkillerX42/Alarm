#!/usr/bin/env python3
import glob
import numpy as np
import time
import datetime
import sys
import os
from morning_weather import Weather
from gtts import gTTS

start = datetime.datetime.now()
print("Alarm started at {}".format(start))
try:
    wavs = glob.glob("/media/pi/SHODAN/Music/*.wav")
    mp3s = glob.glob("/media/pi/SHODAN/Music/*.mp3")
    songs = np.array(wavs + mp3s)
    np.random.shuffle(songs)
    print("    There are {} songs".format(len(songs)))
    played_weather = False
    for song in songs:
        print("    Playing {}".format(song))
        os.system('play -q -v 0.45 "{}"'.format(song))
        now = datetime.datetime.now()
        dt = now - start
        if (dt.seconds >= 30*60) and not played_weather:
            report = Weather()
            tts = gTTS(text=report.forecast, lang='en')
            tts.save("forecast.mp3")
            os.system("play -q forecast.mp3")
            os.system("rm forecast.mp3")
            played_weather = True
        if dt.seconds >= 1.5*3600:
            sys.exit()
except Exception as e:
    print(e)

