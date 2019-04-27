#!/usr/bin/env python3
import glob
import numpy as np
import datetime
import sys
import subprocess as sub
from morning_weather import Weather
# from gtts import gTTS
import starcoder42 as s


class AlarmClock:
    """An alarm clock for personal use, it will run through the songs for a
    desired amount of time, as given in an argument
    """
    def __init__(self):
        self.start = datetime.datetime.now()
        s.iprint("Alarm started at {}".format(self.start), 0)
        wavs = glob.glob("/media/pi/SHODAN/Music/*.wav")
        mp3s = glob.glob("/media/pi/SHODAN/Music/*.mp3")
        flacs = glob.glob("/media/pi/pi_blue/flacs/*/*.flac")
        self.songs = np.array(wavs + mp3s + flacs)
        np.random.shuffle(self.songs)
        s.iprint("There are {} songs".format(len(self.songs)), 1)
        self.played_weather = False
        self.volume = 0.20
        self.dvol = 0.01

    def play_song(self, song):
        song_data = sub.Popen('sox "{}" -n stat'.format(song), shell=True,
                              stderr=sub.PIPE).stderr.readlines()
        vol_lvl = float(song_data[6].split()[-1])
        sub.call('play -q -v {} "{}"'.format(self.volume/vol_lvl, song),
                  shell=True)
        now = datetime.datetime.now()
        dt = now - self.start
        return dt

    def run(self):
        for song in self.songs:
            s.iprint("Playing {}".format(song), 1)
            dt = self.play_song(song)

            if dt.seconds >= 30*60:
                if not self.played_weather:
                    self.play_weather()
                    self.played_weather = True
                self.volume += self.dvol
            if dt.seconds >= 1.5*3600:
                sys.exit()

    def play_weather(self):
        report = Weather()
        report.make_mp3()
        report.play_forecast()


def main():
    alarm = AlarmClock()
    alarm.run()


if __name__ == '__main__':
    main()
