#!/usr/bin/env python3
import numpy as np
import time
import sys
import argparse
import subprocess as sub
from pathlib import Path
import starcoder42 as s
from morning_weather import Weather
from PiTools import fairy_lights


class AlarmClock:
    """An alarm clock for personal use, it will run through the songs for a
    desired amount of time, as given in an argument
    """

    def __init__(self, flacs, wavs, mp3s, screensaver=False, cec=False,
                 lights=False):
        self.flacs = flacs
        self.wavs = wavs
        self.mp3s = mp3s
        self.screensaver = screensaver
        self.cec = cec
        self.lights = lights

        self.start = time.time()
        s.iprint("[{:12.0f}] Alarm started".format(self.start), 0)
        
        sub.call('amixer set PCM -- 85%', shell=True)

        if self.cec:
            tv_on = sub.call('echo "on 0" | cec-client -s -d 1 -p 3',
                             shell=True)
            s.iprint(f"[{time.time():12.0f}] TV turn on exit code: {tv_on}", 1)
            time.sleep(20)
            tv_source = sub.call('echo "as 0" | cec-client -s -d 1 -p 3',
                                 shell=True)
            s.iprint(f"[{time.time():12.0f}] TV switch source exit code"
                     f" {tv_source}", 1)
            # Set volume to 16
            # sub.call('echo "voldown 0" | cec-client -s -d 1 -p 1', shell=True)
            # sub.call('echo "volup 16" | cec-client -s -d 1 -p 1', shell=True)
        
        self.songs = np.array(list(self.wavs)
                              + list(self.mp3s)
                              + list(self.flacs))

        np.random.shuffle(self.songs)
        s.iprint("[{:12.0f}] There are {} songs"
                 "".format(time.time(), len(self.songs)), 1)
        self.played_weather = False
        self.volume_init = 0.04
        self.volume_final = 0.095
        self.volume = self.volume_init
        if self.screensaver:
            sub.call('xscreensaver-command -activate', shell=True)
        if self.lights:
            self.lights = fairy_lights.Lights(23)
            self.lights.on()

    def try_bluetooth(self):
        nearby_devices = bt.discover_devices(lookup_names=True)
        for addr, nam in nearby_devices:
            if '6820' in nam:
                sock = bt.BluetoothSocket(bt.RFCOMM)
                sock.connect((addr, 1))

    def play_song(self, song):
        song_data = sub.Popen('sox "{}" -n stat'.format(song), shell=True,
                              stderr=sub.PIPE).stderr.readlines()
        # print(song_data)
        vol_lvl = float(song_data[6].split()[-1])
        # print(self.volume/vol_lvl)
        res = sub.call('play -q -v {} "{}"'.format(self.volume/vol_lvl, song),
                       shell=True)
        now = time.time()
        dt = now - self.start
        return dt

    def run(self):
        for song in self.songs:
            s.iprint("[{:12.0f}] Playing {} at volume {:.3f}"
            "".format(time.time(), song.name, self.volume), 1)
            # p = Process(self.try_bluetooth())
            # p.start()
            dt = self.play_song(song)
            # p.join()

            if dt < 60 * 60:
                self.volume = (self.volume_init + (self.volume_final
                                                   - self.volume_init)
                               * dt / 60 / 60)
            else:
                self.volume = self.volume_final
                if not self.played_weather:
                    try:
                        self.play_weather()
                        self.played_weather = True
                    except Exception as e:
                        print(e)
                        self.played_weather = True
            
            if dt >= 3 * 3600:
                return 0

    def play_weather(self):
        report = Weather()
        report.convert_units()
        report.make_mp3()
        report.play_forecast()
        report.send_daily('beancc_weather.key')

    def stop(self):
        if self.screensaver:
            sub.call('xscreensaver-command -deactivate', shell=True) 
        if self.cec:
            sub.call('echo "standby 0" | cec-client -s -d 1 -p 3', shell=True)        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--paths', nargs='+', help='Paths with music in'
                                                         ' them')
    parser.add_argument('-s', '--screensaver', action='store_true',
                            default=False, help='Whether or not to use'
                            'xscreensaver during the alarm')
    parser.add_argument('-c', '--cec', action='store_true', default=False,
                        help='Whether or not to issue cec commands to a TV')
    parser.add_argument("-l", "--lights", action="store_true", default=False,
                        help="Turn on the fairy lights with the alarm")
    args = parser.parse_args()
    flacs = []
    wavs = []
    mp3s = []
    for path in args.paths:
        flacs += list(Path(path).rglob('*.flac'))
        wavs += list(Path(path).rglob('*.wav'))
        mp3s += list(Path(path).rglob('*.mp3'))
    alarm = AlarmClock(flacs, wavs, mp3s, screensaver=args.screensaver,
                       cec=args.cec, lights=args.lights)
    alarm.run()
    alarm.stop()

if __name__ == '__main__':
    main()

