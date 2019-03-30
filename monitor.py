import time
from datetime import datetime
from temp_humid import get_temperature_and_humidity
from microclimate_validator import validate_climate
from db import engine, measurements
from logger import logger

while True:
    temperature, humidity = get_temperature_and_humidity()
    measurement = {
        'temperature': temperature,
        'humidity': humidity,
        'is_valid': validate_climate(temperature, humidity),
        'datatime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    conn = engine.connect()
    ins = measurements.insert().values(**measurement)
    logger.info(f'T:{temperature} C  H:{humidity}%')
    time.sleep(5)
