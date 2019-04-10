from sensors import get_measurement
from microclimate_validator import validate_climate
from db import measurements_insert, mean_of_last_n_measurements
from logger import logger, initialize_logger
from mail_sender import MailSender, sender, receiver_email
from timing import MonitorTimer
from config import Config


def main():
    initialize_logger('pimicroclimate.log')

    MONITORED_VALUES = ('temperature', 'humidity')
    mail_sender = MailSender(sender, receiver_email, MONITORED_VALUES)
    monitor_timer = MonitorTimer()

    for _ in monitor_timer.run_forever():
        counter = 0
        measurement = get_measurement()
        temperature, humidity = measurement['temperature'], measurement['humidity']
        is_valid = not bool(validate_climate(temperature, humidity))
        measurement['is_valid'] = is_valid
        measurements_insert(**measurement)

        logger.info(f'T:{temperature} C H:{humidity}% VALID:{is_valid}')

        if counter >= Config.min_measurements_count:
            avg_temp, avg_hum = mean_of_last_n_measurements(Config.min_measurements_count)
            invalid_measurements = validate_climate(avg_temp, avg_hum)

            if invalid_measurements:
                mail_sender.send_email(invalid_measurements)
        else:
            counter += 1


if __name__ == '__main__':
    main()
