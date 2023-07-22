import logging
from requests import Response, get
from pprint import pformat

class WeatherApi:
    """WeatherApi class utilizes the WeatherApi to get the data for the
    weather, given the location details.
    
    WeatherAPI supports four types of requests:
    - Future forcasts:
        range from 14-days to 300-days in
        the future from present day.
    - Todays Forecasts:
        Each hour conditions for whole day.
    - History forecasts:
        upto 365-days in past.
    - Current Weather Conditions.
    
    CONSTANTS:
    ---------
    
    - __BASE_URL
    - __CURRENT_WEATHER_ENDPOINT
    - __HISTORY_ENDPOINT
    - __FUTURE_ENDPOINT
    - __FORECAST_ENDPOINT
    
    Methods:
    -------
    
    current_weather(city_name)
        logs the current weather conditions
    
    todays_forcast(city_name)
        logs the forecast for today with 3 hour interval for whole day
    
    future_forecast(city_name, date)
        logs the forecast with 3h interval for future date (yyyy-mm-dd)
    
    past_weather(city_name, date)
        logs the forecast with 3h interval for past date (yyyy-mm-dd)
    
    NOTE: All the logs can be found in the ./weather-api-requests.log
    """
    
    # CONSTANTS
    __BASE_URL = 'http://api.weatherapi.com/v1'
    __CURRENT_WEATHER_ENDPOINT = '/current.json'
    __HISTORY_ENDPOINT = '/history.json'
    __FUTURE_ENDPOINT = '/future.json'
    __FORECAST_ENDPOINT = '/forecast.json'    
    
    def __init__(self, key) -> None:
        self.__API_KEY = key

        # Logger Configuration
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler('./weather_api_requests.log')
        self.logger.addHandler(self.file_handler)
    
    # Methods
    def current_weather(self, city):
        try:
            url = (
                f"{self.__BASE_URL}{self.__CURRENT_WEATHER_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except Exception as e:
            self.logger.error(e)

    def todays_forcast(self, city):
        try:
            url = (
                f"{self.__BASE_URL}{self.__FORECAST_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except Exception as e:
            self.logger.error(e)

    def future_forecast(self, city, date):
        try:
            url = (
                f"{self.__BASE_URL}{self.__FUTURE_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}&dt={date}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except Exception as e:
            self.logger.error(e)

    def past_weather(self, city, date):
        try:
            url = (
                f"{self.__BASE_URL}{self.__HISTORY_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}&dt={date}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    weather = WeatherApi('52ad3593c0d84e758dc175340232107')
    weather.current_weather('Islamabad')
    weather.todays_forcast('Islamabad')
    weather.future_forecast('Islamabad', '2023-08-23')