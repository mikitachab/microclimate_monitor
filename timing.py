import time
from datetime import datetime
from config import config


class MonitorTimer:
    def __init__(self):
        self.sleep_time = config['default_sleep_time']

    def run_forever(self):
        while True:
            yield
            time.sleep(self.sleep_time)

    def reset_timer(self):
        self.sleep_time = config['default_sleep_time']

    @staticmethod
    def get_current_time():
        now = datetime.now()
        return ':'.join((str(now.hour), str(now.minute)))
