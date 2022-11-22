import os

from pyowm import OWM
from pyowm.commons.exceptions import PyOWMError
from pyowm.utils.config import get_default_config
from dotenv import load_dotenv
from static import messages

load_dotenv()


class WeatherAPI:
    config_dict = get_default_config()
    config_dict['connection']['use_ssl'] = False
    config_dict['connection']["verify_ssl_certs"] = False
    config_dict['language'] = 'ru'
    mgr = None

    def __init__(self):
        owm = OWM(os.getenv('PYOWM_KEY'), self.config_dict)
        self.mgr = owm.weather_manager()

    def get_weather(self, place):
        try:
            observation = self.mgr.weather_at_place(place)
            w = observation.weather
            temp = w.temperature('celsius')['temp']
            feel_like = w.temperature('celsius')['feels_like']
            status = w.detailed_status
            wind = w.wind()['speed']
            return messages.weather_info % (place, str(temp), str(feel_like), status, str(wind))
        except PyOWMError:
            return messages.not_a_place
        except:
            return messages.went_wrong
