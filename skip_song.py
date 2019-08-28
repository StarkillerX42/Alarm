#!/usr/bin/env python3
import subprocess as sub
import numpy as np
import starcoder42 as s

s.iprint('Skipping song', 1)
sub.call('ps auxf > procs.txt', shell=True)
with open("procs.txt", "r") as proc_fil:
    lines = np.array(proc_fil.readlines())
is_song = np.array(["play" in proc for proc in lines])
to_kill = lines[is_song]
for proc in to_kill:
    # print(proc)
    pid = proc.split()[1]
    # print(pid)
    sub.call(['kill', pid])
sub.call(['rm', 'procs.txt'])
