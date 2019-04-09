#!/usr/bin/env python3

import requests
import os
from gtts import gTTS
from slackclient import SlackClient
import starcoder42 as s
from bs4 import BeautifulSoup


class Weather:
    def __init__(self):

        noaa_url = ("https://forecast.weather.gov/MapClick.php?site=BOU&text"
                    "Field1=40.0269&textField2=-105.251")
        noaa_page = BeautifulSoup(requests.get(noaa_url).text, 'html.parser')
        forecasts = noaa_page.find('ul', attrs={'id': 'seven-day-forecast-list'})
        today = list(forecasts)[0]
        img = today.find('img')
        self.forecast = img.attrs['alt']
    
    def convert_units(self):
        first_sentence = self.forecast.split('.')[0]
        temp_fs = []
        for i, word in enumerate(first_sentence.split(' ')):
            try:  # Appends numbers to a list, but keeps them as strings
                int(word)
                temp_fs.append(word)
            except ValueError:
                pass
        for i, temp_f in enumerate(temp_fs):
            temp_c = s.fahr2cel(temp_f)
            self.forecast.replace(temp, str(temp_c))
    def make_mp3(self, filename: str = "forecast.mp3"):
        self.filename = filename
        tts = gTTS(text=self.forecast, lang="en")
        tts.save(filename)
    
    def play_forecast(self):
        os.system("play -q {}".format(self.filename))
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
