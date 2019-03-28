#!/usr/bin/env python3

import requests
import os
from gtts import gTTS
from slackclient import SlackClient
import starcoder42 as s


class Weather:
    def __init__(self):

        noaa_url = ("https://forecast.weather.gov/MapClick.php?site=BOU&text"
                    "Field1=40.0269&textField2=-105.251")
        noaa_page = requests.get(noaa_url).text.split("\n")
        subset_ind = noaa_page.index("<!-- 7-Day Forecast -->")
        subset = noaa_page[subset_ind:subset_ind+15]
        # print(subset[11])
        self.forecast = subset[11].split('alt="')[1].split('. "')[0].split(": ")[1]
    
    def make_mp3(self, filename: str = "forecast.mp3"):
        self.filename = filename
        tts = gTTS(text=self.forecast, lang="en")
        tts.save(filename)
    
    def play_forecast(self):
        os.system("play {}".format(self.filename))
        os.system("rm {}".format(self.filename))

    def send_daily(self, key_file="oauth.key"):
        key = open(key_file, "r").read()
        sc = SlackClient(key)
        response = sc.api_call("chat.postMessage", channel="@dylan.gatlin",
                               text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Jordan Gage", text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Nicholas Rahne", text=self.forecast)
        # response = sc.api_call("chat.postMessage",
        #                        channel="@Michael Haney", text=self.forecast)
        return response


def main():
    report = Weather()
    response = report.send_daily()
    if response["ok"]:
        pass
    else:
        s.iprint(response["error"], 1)


if __name__ == "__main__":
    main()
