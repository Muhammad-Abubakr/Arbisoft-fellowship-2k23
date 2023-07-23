import logging
from requests import Response, get
from pprint import pformat

class WeatherApi:
    """WeatherApi class utilizes the WeatherApi to get the data for the
    weather, given the location details.
    
    WeatherAPI supports four types of requests:
    - Future forcasts.
    - Today's Forecasts.
    - History forecasts.
    - Current Weather Conditions.
    
    ### Methods:
    
    current_weather(city_name)
        logs the current weather conditions
    
    todays_forcast(city_name)
        logs the forecast for present day
    
    future_forecast(city_name, date)
        logs the predicted forecast future date (yyyy-mm-dd)
    
    history_forecast(city_name, date)
        logs the forecast for the given date (yyyy-mm-dd) from past
    
    NOTE: All the logs can be found in the ./weather.log
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
        logging.basicConfig(
            filename='weather.log',
            format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
            datefmt='%Y-%m-%d at %H:%M:%S',
            level=logging.DEBUG
        )
        self.logger = logging.getLogger(__name__)
        
        # self.formatter = logging.Formatter(
        #     '%(levelname)s:%(asctime)s:%(message)s',
        #     datefmt='%Y-%m-%d at %H:%M:%S')
        # self.file_handler = logging.FileHandler(filename='weather.log')
        # self.file_handler.setFormatter(self.formatter)
        # self.logger.addHandler(self.file_handler)
        # self.logger.setLevel(logging.DEBUG)
     
    # Methods
    def current_weather(self, city):
        self.logger.info("Sending request for current weather conditions...")
        
        try:
            url = (
                f"{self.__BASE_URL}{self.__CURRENT_WEATHER_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}"
            )
            res = get(url)
            parsed = Response.json(res)
            
            # repr_str = f""" Current Weather Conditions
            # Cloudiness: {parsed['cloud']}%
            # Condition: {parsed['condition']['text']}
            # Temperature: {parsed['temp_c']} C
            # Feels Like: {parsed['feelslike_c']} C
            # Wind: {parsed['wind_kph']} kph
            # Humidity: {parsed['humidity']}%
            # Precipitation: {parsed['precip_mm']} mm
            # """
            # self.logger.info(repr_str)
            
            self.logger.info(pformat(parsed))
                        
        except BaseException as e:
            self.logger.error("An Error occured while making the request!")

    def todays_forcast(self, city):
        self.logger.info("Sending request for Today's forecast...")

        try:
            url = (
                f"{self.__BASE_URL}{self.__FORECAST_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except BaseException as e:
            self.logger.error("An Error occured while making the request!")

    def future_forecast(self, city, date):
        self.logger.info(f"Sending request for predicted {date} Forecast...")

        try:
            url = (
                f"{self.__BASE_URL}{self.__FUTURE_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}&dt={date}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except BaseException as e:
            self.logger.error("An Error occured while making the request!")

    def history_forecast(self, city, date):
        self.logger.info(f"Sending request for past {date} forecast...")

        try:
            url = (
                f"{self.__BASE_URL}{self.__HISTORY_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}&dt={date}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))
            
        except BaseException as e:
            self.logger.error("An Error occured while making the request!")


if __name__ == '__main__':
    weather = WeatherApi('52ad3593c0d84e758dc175340232107')
    weather.current_weather('Islamabad')
    weather.todays_forcast('Islamabad')
    weather.future_forecast('Islamabad', '2023-08-23')
    weather.history_forecast('Islamabad', '2023-06-23')