#!/home/pi/berryconda3/bin/python
import numpy as np
import datetime
import sys
import bluetooth as bt
import subprocess as sub
from pathlib import Path
import starcoder42 as s
from morning_weather import Weather
from multiprocess import Process


class AlarmClock:
    """An alarm clock for personal use, it will run through the songs for a
    desired amount of time, as given in an argument
    """

    def __init__(self):
        self.start = datetime.datetime.now()
        s.iprint("Alarm started at {}".format(self.start), 0)
        shodan = Path('/media/pi/SHODAN/Music/')
        wavs = shodan.rglob('*.wav')
        mp3s = shodan.rglob('*.wav')
        flacs = Path('/media/pi/pi_red/flac/').rglob('*.flac')
        self.songs = np.array(list(wavs) + list(mp3s) + list(flacs))
        np.random.shuffle(self.songs)
        s.iprint("There are {} songs".format(len(self.songs)), 1)
        self.played_weather = False
        self.volume_init = 0.05
        self.volume_final = 0.14
        self.volume = self.volume_init

    def try_bluetooth(self):
        nearby_devices = bt.discover_devices(lookup_names=True)
        for addr, nam in nearby_devices:
            if '6820' in nam:
                sock = bt.BluetoothSocket(bt.RFCOMM)
                sock.connect((addr, 1))

    def play_song(self, song):
        song_data = sub.Popen('sox "{}" -n stat'.format(song), shell=True,
                              stderr=sub.PIPE).stderr.readlines()
        vol_lvl = float(song_data[6].split()[-1])
        sub.call('play -q -v {} "{}"'.format(self.volume / vol_lvl, song),
                 shell=True)
        # print(self.volume/vol_lvl)
        now = datetime.datetime.now()
        dt = now - self.start
        return dt

    def run(self):
        for song in self.songs:
            s.iprint("Playing {}".format(song), 1)
            p = Process(self.try_bluetooth())
            p.start()
            dt = self.play_song(song)
            p.join()

            if dt.seconds >= 30 * 60:
                if not self.played_weather:
                    try:
                        self.play_weather()
                        self.played_weather = True
                    except Exception as e:
                        print(e)
                        self.played_weather = True
                self.volume = (self.volume_init + (self.volume_final
                                                   - self.volume_init)
                               * dt.seconds / 30 / 60)
            else:
                self.volume = self.volume_final

            if dt.seconds >= 1.5 * 3600:
                sys.exit()

    def play_weather(self):
        report = Weather()
        report.make_mp3()
        report.play_forecast()
        report.send_dailty()

def main():
    alarm = AlarmClock()
    alarm.run()


if __name__ == '__main__':
    main()
