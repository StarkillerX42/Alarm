#!/usr/bin/env python3
import numpy as np
import os
print("Stopping alarm.py")
os.system("ps auxf > procs.txt")
with open("procs.txt", "r") as proc_fil:
    lines = np.array(proc_fil.readlines())
is_alarm = np.array([("/alarm.py" in proc)
                     or (" play " in proc)
                     for proc in lines])
to_kill = lines[is_alarm]
print(to_kill)
for proc in to_kill:
    # print(proc)
    id = proc.split()[1]
    # print(id)
    os.system("kill {}".format(id))
os.system("rm procs.txt")
