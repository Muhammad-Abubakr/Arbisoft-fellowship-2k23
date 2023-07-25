import logging
from requests import Response, get
from pprint import pformat
import argparse
import constants
import datetime


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
    __BASE_URL = "http://api.weatherapi.com/v1"
    __CURRENT_WEATHER_ENDPOINT = "/current.json"
    __HISTORY_ENDPOINT = "/history.json"
    __FUTURE_ENDPOINT = "/future.json"
    __FORECAST_ENDPOINT = "/forecast.json"

    def __init__(self, key: str) -> None:
        """Intializes the WeatherApi object with the given API_KEY, also
        configures the root logger to log the information received from the
        API after making the requests into the log file.
        """
        self.__API_KEY = key

        # Logger Configuration
        logging.basicConfig(
            filename="weather.log",
            format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
            datefmt="%Y-%m-%d at %H:%M:%S",
            level=logging.DEBUG,
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
    def current_weather(self, city: str) -> None:
        """logs the current weather information received from the weather api
        to the log file.

            Parameters:
                city (str): Name of the city e.g Islamabad, Lahore

            Returns:
                None
        """
        self.logger.info("Sending request for current weather conditions...")

        try:
            url = (
                f"{self.__BASE_URL}{self.__CURRENT_WEATHER_ENDPOINT}?key="
                f"{self.__API_KEY}&q={city}"
            )
            res = get(url)
            parsed = Response.json(res)
            self.logger.info(pformat(parsed))

        except BaseException as e:
            self.logger.error("An Error occured while making the request!")

    def todays_forcast(self, city: str) -> None:
        """Logs the details about present day forecast to the log file, the
        log contains information about whole day conditions and hourly for-
        cast for the queried city.

            Parameters:
                city (str): Name of the City e.g Islamabad, Lahore

            Returns:
                None
        """
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

    def future_forecast(self, city: str, date: str) -> None:
        """Logs the forecast details about the queried future day in the log
        file. The log contains information about the given day whole day con-
        dition and also the hourly forecast for the whole day.

            Parameters:
                city (str): Name of the City e.g Islamabad, Lahore
                date (str): Date in the future for which we need to query the
                        information about, the format must be (yyyy-mm-dd)

            Returns:
                None
        """
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

    def history_forecast(self, city: str, date: str) -> None:
        """Logs the forecast details about the queried past day in the log
        file. The log contains information about the given day whole day con-
        dition and also the hourly forecast for the whole day.

            Parameters:
                city (str): Name of the City e.g Islamabad, Lahore
                date (str): Date in the future for which we need to query the
                        information about, the format must be (yyyy-mm-dd)

            Returns:
                None
        """
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


def weather_date(date: str) -> str:
    """Checks the format for the date as required by the WeatherApi

    Parameters:
        date (str): Date of the day for which the user wants to query

    Returns:
        date (str): Date string that respects the WeatherApi Date Format

    Exceptions:
        TypeError: raised if the date string does not follow WeatherApi
                date format
    """
    try:
        year, month, day = date.split("-")

        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise TypeError

        # Type checking using Type Casting, so that we only have numbers as
        # our year, month and day
        year = int(year)
        month = int(month)
        day = int(day)

        return date

    except TypeError:
        raise argparse.ArgumentTypeError(
            f"The date must be of format (yyyy-mm-dd) given {date}"
        )


if __name__ == "__main__":
    weather = WeatherApi(constants.API_KEY)

    # Arugments Parser
    parser = argparse.ArgumentParser()

    # argparse configuration
    # --city CITY required
    parser.add_argument(
        "--city",
        type=str,
        required=True,
        help="Name of the city you want to query the information about.",
    )
    # --date DATE optional
    parser.add_argument(
        "--date",
        type=weather_date,
        required=False,
        help="Date for the day you want to query the forecast information.",
    )
    # --time required choices=(
    #                   "history", "future",
    #                   "todays-forecast", "current-climate")
    parser.add_argument(
        "--time",
        required=True,
        choices=["history", "future", "todays-forecast", "current-climate"],
        help=(
            "Time can be any of the four choices. `history` and `future`"
            "arguments require date"
        ),
    )

    # parsing the command line arguments
    args = parser.parse_args()

    # Checking if we have a time flag that requires date flag to be set
    if args.time in ["history", "future"] and args.date is None:
        raise argparse.ArgumentTypeError(
            "`history` and `future` time arguments require --date to be set"
        )

    # Calling the appropriate method based on the flags passed to the script
    if args.time in ["history", "future"]:
        if args.time == "history":
            weather.history_forecast(args.city, args.date)
        else:
            weather.future_forecast(args.city, args.date)
    elif args.time == "current-climate":
        weather.current_weather(args.city)
    else:
        weather.todays_forcast(args.city)
