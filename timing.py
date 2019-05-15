import time
from datetime import datetime
from config import config


class MonitorTimer:
    def __init__(self):
        self.sleep_time = config['default_sleep_time']
        self.reduced_sleep_time = self.sleep_time / config['measurements_frequency_multiplier']
        self.increase_measurement_rate = False

    def run_forever(self):
        while True:
            yield
            if self.increase_measurement_rate:
                time.sleep(self.reduced_sleep_time)
            else:
                time.sleep(self.sleep_time)

    def higher_frequency_timer(self):
        time.sleep(self.reduced_sleep_time)

    def reset_timer(self):
        self.sleep_time = config['default_sleep_time']
        self.reduced_sleep_time = self.sleep_time / config['measurements_frequency_multiplier']

    @staticmethod
    def get_current_time():
        now = datetime.now()
        return ':'.join((str(now.hour), str(now.minute)))
