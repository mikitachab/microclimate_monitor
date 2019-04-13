from sensors import get_measurement
from microclimate_validator import validate_climate
from db import measurements_insert, mean_of_last_n_measurements
from logger import logger, initialize_logger
from mail_sender import MailSender, sender,
from timing import MonitorTimer
from config import Config


def main():
    initialize_logger('pimicroclimate.log')

    MONITORED_VALUES = ('temperature', 'humidity')
    mail_sender = MailSender(sender, Config.receiver_email, MONITORED_VALUES)
    monitor_timer = MonitorTimer()
    counter = 1
    for _ in monitor_timer.run_forever():
        measurement = get_measurement()
        temperature, humidity = measurement['temperature'], measurement['humidity']
        is_valid = not bool(validate_climate(temperature, humidity))
        measurement['is_valid'] = is_valid
        measurements_insert(**measurement)

        logger.info(f'T:{temperature} C H:{humidity}% VALID:{is_valid}')

        if counter >= Config.min_measurements_count:
            counter = 1
            avg_temp, avg_hum = mean_of_last_n_measurements(Config.min_measurements_count)
            logger.info(f'AVG_TEMP: {avg_temp}, AVG_HUM {avg_hum}')
            invalid_measurements = validate_climate(avg_temp, avg_hum)

            if invalid_measurements:
                mail_sender.send_email(invalid_measurements)
        else:
            counter += 1


if __name__ == '__main__':
    main()
