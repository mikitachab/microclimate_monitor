import time
from datetime import datetime
from temp_humid import get_temperature_and_humidity
from microclimate_validator import validate_climate
from db import engine, measurements
from logger import logger
from pi_email import send_email, test_receiver_email

message  = """\
Subject: microclimate

Hi, something wrong with your microclimate. It's time to something
This message is sent from Python.
Rasberry Pi started monitoring.
"""

while True:
    temperature, humidity = get_temperature_and_humidity()
    is_valid = validate_climate(temperature, humidity)
    measurement = {
        'temperature': temperature,
        'humidity': humidity,
        'is_valid': is_valid,
        'datetime': datetime.now().replace(microsecond=0)
    }
    conn = engine.connect()
    ins = measurements.insert().values(**measurement)
    conn.execute(ins)
    logger.info(f'T:{temperature} C H:{humidity}% VALID:{is_valid}')
    if not is_valid:
        send_email(test_receiver_email, message)
    time.sleep(60)
