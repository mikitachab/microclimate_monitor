from sensors import get_measurement
from microclimate_validator import validate_climate
from db import measurements_insert, mean_of_last_n_measurements
from logger import logger, initialize_logger
from mail_sender import MailSender
from timing import MonitorTimer
from config import config


class Monitor():
    def __init__(self):
        self._last_invalid_measurements = {}
        self._mail_sender = MailSender(
            config['sender'], config['receiver_email'], config['MONITORED_VALUES'])
        self._timer = MonitorTimer()

    def run(self):
        for _ in self._timer.run_forever():
            self._tick()

    def _tick(self):
        is_valid = self._receive_and_check_measurements()

        if not is_valid:
            self._timer.run_more_frequently = True

        if self._timer.tick_main_counter() == config['min_measurements_count']:
            invalid_measurements = self._validate_last_measurements()
            if invalid_measurements and self._last_invalid_measurements != invalid_measurements:
                self._mail_sender.send_alarming_email(invalid_measurements)
                last_invalid_measurements = invalid_measurements
                self._timer.reset_reminder_counter()
            elif last_invalid_measurements:
                self._mail_sender.send_praising_email()
                last_invalid_measurements.clear()
                self._timer.reset_reminder_counter()

        if last_invalid_measurements and self._timer.tick_reminder_counter() == config['remind_time']:
            self._mail_sender.send_reminding_email(
                last_invalid_measurements)
            self._timer.reset_reminder_counter()

        current_hour = MonitorTimer.get_current_time()
        if current_hour == config['notification_time']:
            self._mail_sender.send_informing_mail(get_measurement())

    def _receive_and_check_measurements(self):
        measurement = get_measurement()
        temperature, humidity = measurement['temperature'], measurement['humidity']
        is_valid = not bool(validate_climate(temperature, humidity))
        measurement['is_valid'] = is_valid
        measurements_insert(**measurement)

        logger.info(f'T:{temperature} C H:{humidity}% VALID:{is_valid}')
        return is_valid

    def _validate_last_measurements(self):
        self._timer.reset_main_counter()
        self._timer.run_more_frequently = False
        avg_temp, avg_hum = mean_of_last_n_measurements(
            config['min_measurements_count'])

        logger.info(f'AVG_TEMP: {avg_temp}, AVG_HUM {avg_hum}')
        return validate_climate(avg_temp, avg_hum)


def main():
    initialize_logger('pimicroclimate.log')

    Monitor().run()


if __name__ == '__main__':
    main()
