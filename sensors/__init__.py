from datetime import datetime
from temp_humid import get_temperature_and_humidity


def get_measurement():
    temperature, humidity = get_temperature_and_humidity()
    measurement = {
        'temperature': temperature,
        'humidity': humidity,
        'datetime': datetime.now().replace(microsecond=0)
    }
    return measurement
