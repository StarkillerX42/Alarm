#!/usr/bin/env python3
import numpy as np
import subprocess as sub
from PiTools import fairy_lights

print("Stopping alarm.py")
procs = sub.Popen("ps auxf", stdout=sub.PIPE, shell=True)
lines = np.array(procs.stdout.read().decode('utf-8').splitlines())
is_alarm = np.array([("/alarm.py" in str(proc))
                     or (" play " in str(proc))
                     for proc in lines])
to_kill = lines[is_alarm]
# print(to_kill)
for proc in to_kill:
    # print(proc)
    id = proc.split()[1]
    # print(id)
    sub.call("kill {}".format(id), shell=True)
# sub.call('echo "standby 0" | cec-client -s -d 1 -p 3', shell=True)

lights = fairy_lights.Lights(23)
lights.off()

