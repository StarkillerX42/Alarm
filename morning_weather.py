#!/usr/bin/env python3

import requests
import time
import os
import numpy as np
from gtts import gTTS
from slackclient import SlackClient
import starcoder42 as s
class Weather:
    def __init__(self):

        noaa_url = ("https://forecast.weather.gov/MapClick.php?site=BOU&textField1=40.0"
                    "269&textField2=-105.251")
        noaa_page = requests.get(noaa_url).text.split("\n")
        subset_ind = noaa_page.index("<!-- 7-Day Forecast -->")
        subset = noaa_page[subset_ind:subset_ind+15]
        # print(subset[11])
        self.forecast = subset[11].split('alt="')[1].split('. "')[0].split(": ")[1]
    
    def make_mp3(filename:str="forecast.mp3"):
        self.filename = filename
        tts = gTTS(text=self.forecast, lang="en")
        tts.save(filename)
    
    def play_forecast(self):
        os.system("play {}".format(self.filename))

    def send_daily(self):
        sc = SlackClient("xoxb-329888754887-33KgV85uLazdCKxGDI6Dx9eG")
        response = sc.api_call("chat.postMessage",
                               channel="@dylan.gatlin", text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Jordan Gage", text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Nicholas Rahne", text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Michael Haney", text=self.forecast)



        if response["ok"]:
            pass
        else:
            s.iprint(response["error"], 1)

def main():
    report = Weather()
    report.send_daily()

if __name__ == "__main__":
    main()
