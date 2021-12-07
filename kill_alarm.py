#!/usr/bin/env python3
import subprocess as sub
import numpy as np
import time
from PiTools import fairy_lights

procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
lines = np.array(procs.stdout.read().decode('utf-8').splitlines())
is_alarm = np.array([("/alarm.py" in str(proc))
                     for proc in lines])
to_kill = lines[is_alarm]

for proc in to_kill:
    # print(proc)
    pid = proc.split()[1]
    # print(pid)
    sub.call(['kill', pid])

lights = fairy_lights.Lights(17)
lights.off()
# time.sleep(200)
# import now_kill_alarm
# sub.call('xscreensaver-command -deactivate', shell=True)
# sub.call('echo standby 0 | cec-client -s -d 1 -p 3', shell=True)

