import os

config = {
        'default_sleep_time': 2,
    'min_measurements_count': 5,
    'receiver_email': 'zpiseminar@gmail.com',
    'MONITORED_VALUES': ('temperature', 'humidity', 'light'),
    'ssl_port': 465,
    'smtp_server': 'smtp.gmail.com',
    'sender': {
        'mail': 'microclimatepi@gmail.com',
        'password': os.environ.get('GMAIL_PASS'),
    }
}
