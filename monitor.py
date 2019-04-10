import time
from statistics import mean
from sensors import get_measurement
from microclimate_validator import validate_climate
from db import engine, measurements_insert
from logger import logger, initialize_logger
from mail_sender import MailSender, sender, receiver_email
from timing import MonitorTimer


def main():
    MONITORED_VALUES = ('temperature', 'humidity')
    mail_sender = MailSender(sender, receiver_email, MONITORED_VALUES)

    initialize_logger('pimicroclimate.log')

    temperatures = []
    humidity_list = []

    monitor_timer = MonitorTimer()

    for _ in monitor_timer.run_forever():
        measurement = get_measurement()
        temperature, humidity = measurement['temperature'], measurement['humidity']

        temperatures.append(temperature)
        humidity_list.append(humidity)

        is_valid = not bool(validate_climate(temperature, humidity))

        measurement['is_valid'] = is_valid

        measurements_insert(**measurement)

        logger.info(f'T:{temperature} C H:{humidity}% VALID:{is_valid}')

        if len(temperatures) == 5:
            avg_temp = mean(temperatures)
            avg_hum = mean(humidity_list)
            invalid_measurements = validate_climate(avg_temp, avg_hum)

            if invalid_measurements:
                mail_sender.send_email(invalid_measurements)

            temperatures.clear()
            humidity_list.clear()


if __name__ == '__main__':
    main()
