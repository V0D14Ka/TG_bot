from pyowm import OWM
from pyowm.commons.exceptions import PyOWMError
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['connection']['use_ssl'] = False
config_dict['connection']["verify_ssl_certs"] = False
config_dict['language'] = 'ru'

owm = OWM('c16d779e903477e532485d9034029c6f', config_dict)
mgr = owm.weather_manager()


def get_weather(place):
    try:
        observation = mgr.weather_at_place(place)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        feel_like = w.temperature('celsius')['feels_like']
        status = w.detailed_status
        wind = w.wind()['speed']
        return ('Сегодня в городе - ' + place + '🏙:\n'
                + '❄️Температура воздуха:' + ' ' + str(temp) + '°.' + '\n'
                + '🤨 Ощущается как: ' + str(feel_like) + '°.' + '\n'
                + '✅ Статус: ' + status + '.\n'
                + '💨 Порывы ветра достигают: ' + str(wind) + ' м/с.')
    except PyOWMError:
        return ('Неккоректный город!😡')
