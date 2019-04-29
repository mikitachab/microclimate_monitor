from datetime import datetime
from sensors.temp_humid import get_temperature, get_humidity
from sensors.light import get_light
from config import config

sensors_map = {
    'temperature': get_temperature,
    'humidity': get_humidity,
    'light': get_light
}


def get_measurement():
    measurement = {
        'datetime': datetime.now().replace(microsecond=0)
    }
    for value in config['MONITORED_VALUES']:
        measurement[value] = sensors_map[value]()
    return measurement
