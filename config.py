import os
import json

default_static_config = {
    'measurements_frequency_multiplier': 5,
    'MONITORED_VALUES': ('temperature', 'humidity', 'light', 'is_loud'),
    'ssl_port': 465,
    'smtp_server': 'smtp.gmail.com',
    'sender': {
        'mail': 'microclimatepi@gmail.com',
        'password': os.environ.get('GMAIL_PASS'),
    },
    'remind_time': 30,
    'test_dedicated_state': False,
    'device_id': 1,
}


class Config:
    def __init__(self, path):
        self.config_path = path
        self.static_config = default_static_config

    def get_config_json(self):
        with open(self.config_path) as config_file:
            return json.loads(config_file.read())

    def get(self, key):
        if key in self.static_config:
            return self.static_config[key]
        else:
            return self.get_config_json()[key]

    def __setitem__(self, idx, value):
        self.static_config[idx] = value

    def __getitem__(self, key):
        return self.get(key)
