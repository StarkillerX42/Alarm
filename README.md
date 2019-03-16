# Alarm Clock

This is my alarm clock for my raspberry pi. it works rather well with my setup, but you'll probably need to make some changes for implimentation on your own pi. for example, my music is stored on a USB called Shodan, which you'll need to change. None of my functions use main, sue me.

## Files
alarm.py runs the alarm, and is a file I run in crontab
alarmkill.py is a function that uses pkill to end the alarm early. I have an alias for this in my bashrc called alm, but if you know how, this could be run a number of ways like a gpio button. If you implement a 433 Mhz radio receiver to trigger this, let me know, that's probably the next step for this project.
cec_test.py is an attempt at booting up my TV from my pi while running the alarm, and it was necessary when I had speakers connected to my TV, not my pi, but I never got it to work. Unless you have your pi connected to a TV, this won't matter.

## Known Issues
The pi can run a little hot processing a wave file. pygame seems to br thr best music player, but it really taxes the CPU and runs just below 80deg C. If you can find a more lightweight method, feel free to pull request.

## TODO
Create a weather messenger that uses gTTS to recite the weather in the morning

