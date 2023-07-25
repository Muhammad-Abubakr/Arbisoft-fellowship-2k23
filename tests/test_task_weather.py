import sys
import os

os.chdir('..')
sys.path.append(os.path.join(os.getcwd(), 'tasks', 'weather_api'))

from weather_api import WeatherApi, constants

api: WeatherApi = WeatherApi(constants.API_KEY)