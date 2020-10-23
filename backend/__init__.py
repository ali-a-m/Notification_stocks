import requests
import sounddevice as sd
import time
import librosa as lr
import os
import numpy as np
import pickle as pkl

from requests import Session
from datetime import datetime

class Price:
    
    def __init__(self, symbol):
        if symbol == 'BTC':
            self.__symbol = 0
            self.status = True
        elif symbol == 'ETH':
            self.__symbol = 1
            self.status = True
        else:
            self.status = False

    def get_price(self):

        try:

            bitcoin_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

            parameters = {
                'start':'1',
                'limit':'2',
                'convert':'USD'
            }

            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': '88c2e5b3-cff3-40a0-82d9-b0c8731fad24',
            }

            session = Session()

            session.headers.update(headers)

            response = session.get(bitcoin_api_url, params=parameters)
            response_json = response.json()
            response_json = response_json['data']

            return response_json[self.__symbol]['quote']['USD']['price']
        except:
            return 0

    def thereshold(self, coef, coin_price):
        try:
            min = coin_price - (coin_price * coef)
            max = coin_price + (coin_price * coef)

            return [round(min, 2), round(max, 2)]
        except:
            pass
class Sound:
    
    def __init__(self, sound_file=None, device=None):

        self.sound_file = '' if sound_file == None else sound_file
        if not os.path.exists('backend/dumps/music_array.pkl'):
            self.music_to_array()
        else:
            self.__audio_signal, self.__sample_rate = self.read_music()

        # self.__device = 'SAMSUNG (AMD High Definition Audio Device), Windows DirectSound' if device == None else device
        self.__device = None
    def error(self):
        try:
            time = np.linspace(0,1, 44100*1)
            sound = np.sin(2*np.pi*220*time)

            if not self.__device == None:
                sd.default.device = self.__device

            sd.play(sound)
            sd.wait()
            sd.stop()
        except:
            pass
    def notice_me(self):
        try:
            if not self.__device == None:
                sd.default.device = self.__device
            sd.play(self.__audio_signal, self.__sample_rate)
            sd.wait()
            sd.stop()
        except:
            pass

    def music_to_array(self):
        try:
            s, sr = lr.load(self.sound_file)

            file_ = open('backend/dumps/music_array.pkl', 'wb')
            data = np.array([s, sr])

            pkl.dump(data, file_)
        except Exception as e:
            print(e)

    def read_music(self):
        try:
            file_ = open('backend/dumps/music_array.pkl', 'rb')
            return pkl.load(file_)

        except Exception as e:
            print(e)

class Webhooks:
    
    def __init__(self, IFTTT_URL, symbol=None):
        self.url = IFTTT_URL
        self.symbol = symbol
    
    def send_notice(self, text=None, price=None):
        try:

            if text == None:
                price = round(price, 2)

                self.text = '{} price is at ${} Buy or sell now!'.format(self.symbol, price)
            else:
                self.text = text

            json_data = dict(value1 = self.text)

            response = requests.post(self.url, json=json_data)
            if response.status_code == 200:
                return True 
        except:
            return False
