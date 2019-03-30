import time
from datetime import datetime
from temp_humid import get_temperature_and_humidity
from microclimate_validator import validate_climate
from db import engine, measurements


while True:
    temperature, humidity = get_temperature_and_humidity()
    measurement = {
        'temperature': temperature,
        'humidity': humidity,
        'is_valid': validate_climate(temperature, humidity),
        'datatime': datetime.now().replace(microseconds=0)
    }
    conn = engine.connect()
    ins = measurements.insert().values(**measurement)
    time.sleep(30)
