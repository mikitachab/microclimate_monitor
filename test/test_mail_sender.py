import pytest

from microclimate_validator import InvalidationType
from mail_sender import MailSender
from config import config


@pytest.fixture
def mail_sender():
    return MailSender(config['sender'], config['receiver_email'], ('temperature', 'humidity'))


@pytest.mark.parametrize('measuremements, message', [
    ({
        'temperature': (15, 19, InvalidationType.LOW),
        'humidity': (80, 60, InvalidationType.HIGH)
    },
        'Wrong temperature. It is 15 and should be 19.\n'
        'Consider increasing the temperature.\n'
        '\n'
        'Wrong humidity. It is 80 and should be 60.\n'
        'Consider decreasing the humidity.\n'
    ),
    ({
        'temperature': (50, 26, InvalidationType.HIGH),
    },
        'Wrong temperature. It is 50 and should be 26.\n'
        'Consider decreasing the temperature.\n'
    ),
    ({
        'humidity': (10, 40, InvalidationType.LOW)
    },
        'Wrong humidity. It is 10 and should be 40.\n'
        'Consider increasing the humidity.\n'
    ),
    ({}, '')
])
def test_construct_message(mail_sender, measuremements, message):
    assert mail_sender._construct_message(measuremements) == message
