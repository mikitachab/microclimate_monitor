import pytest

from microclimate_validator import InvalidationType
from mail_builder import MailBuilder, MailType


@pytest.fixture
def mail_builder():
    return MailBuilder(('temperature', 'humidity'))


measurements_and_expected_messages = [
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
    )
]


@pytest.mark.parametrize('measurements, message', measurements_and_expected_messages)
def test_build_alarming_mail(mail_builder, measurements, message):
    assert mail_builder.build_mail(MailType.ALARM, measurements) == \
        'A problem occured with your climate!\n' + message


@pytest.mark.parametrize('measurements, message', measurements_and_expected_messages)
def test_build_reminding_mail(mail_builder, measurements, message):
    assert mail_builder.build_mail(MailType.REMIND, measurements) == \
        'Last problems are still not fixed! Reminder: \n' + message


def test_build_praising_mail(mail_builder):
    assert mail_builder.build_mail(MailType.PRAISE) == \
        'Everything is good with your climate now!\n'


def test_build_informing_mail(mail_builder):
    measurements = {
        'temperature': 666,
        'humidity': 2137
    }
    message = 'Daily message from microclimate monitor. Current climate:\ntemperature: 666\nhumidity: 2137\n'

    assert mail_builder.build_mail(MailType.INFO, measurements) == message
