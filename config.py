import os


class Config:
    default_sleep_time = 60
    gmail_user = 'microclimatepi@gmail.com'
    gmail_pass = os.environ.get('GMAIL_PASS')
    min_measurements_count = 5
