import pytest

from microclimate_validator import InvalidationType
from mail_sender import MailSender, sender, receiver_email


@pytest.fixture
def mail_sender():
    return MailSender(sender, receiver_email, ('temperature', 'humidity'))


@pytest.mark.parametrize('measuremements, message', [
    ({
        'temperature': (15, InvalidationType.LOW),
        'humidity': (80, InvalidationType.HIGH)
    },
        'Wrong temperature. It is 15\n'
        'Consider increasing the temperature.\n'
        '\n'
        'Wrong humidity. It is 80\n'
        'Consider decreasing the humidity.\n'
    ),
    ({
        'temperature': (50, InvalidationType.HIGH),
    },
        'Wrong temperature. It is 50\n'
        'Consider decreasing the temperature.\n'
    ),
    ({
        'humidity': (10, InvalidationType.LOW)
    },
        'Wrong humidity. It is 10\n'
        'Consider increasing the humidity.\n'
    ),
    ({}, '')
])
def test_construct_message(mail_sender, measuremements, message):
    assert mail_sender._construct_message(measuremements) == message
