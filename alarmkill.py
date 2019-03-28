import os
print("Stopping alarm.py")
os.system("ps auxf > procs.txt")
with open("procs.txt", "r") as proc_fil:
    lines = np.array(proc_fil.readlines())
is_alarm = np.array(["/Alarm/alarm.py" in proc for proc in lines])
to_kill = lines[is_alarm]
for proc in to_kill:
    # print(proc)
    id = proc.split()[1]
    # print(id)
    os.system("kill {}".format(id))
os.system("rm procs.txt")
