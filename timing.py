import time
from config import Config


class MonitorTimer:
    def __init__(self):
        self.sleep_time = Config.default_sleep_time

    def run_forever(self):
        while True:
            yield
            time.sleep(self.sleep_time)

    def reset_timer(self):
        self.sleep_time = Config.default_sleep_time
