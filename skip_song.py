#!/usr/bin/env python3
import subprocess as sub
sub.call('ps auxf > procs.txt', shell=True)
with open("procs.txt", "r") as proc_fil:
    lines = np.array(proc_fil.readlines())
is_song = np.array(["play -q -v" in proc for proc in lines])
to_kill = lines[is_song]
for proc in to_kill:
    # print(proc)
    id = proc.split()[1]
    # print(id)
    sub.call(['kill', id])
sub.call(['rm', 'procs.txt'])

