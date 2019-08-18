#!/usr/bin/env python3
import subprocess as sub
import numpy as np

sub.call('ps auxf > procs.txt', shell=True)
with open("procs.txt", "r") as proc_fil:
        lines = np.array(proc_fil.readlines())
is_song = np.array(["/Alarm/alarm.py" in proc for proc in lines])
to_kill = lines[is_song]
for proc in to_kill:
    # print(proc)
    pid = proc.split()[1]
    # print(pid)
    sub.call(['kill', pid])
sub.call(['rm', 'procs.txt'])
sub.call('echo "standby 0" | cec-client -s -d 1', shell=True)

