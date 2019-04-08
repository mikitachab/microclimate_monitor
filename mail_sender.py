import os
import smtplib
import ssl
from microclimate_validator import InvalidationType
from logger import logger

port = 465  # for SSL
smtp_server = 'smtp.gmail.com'
sender = {
    'mail': 'microclimatepi@gmail.com',
    'password': os.environ.get('GMAIL_PASS')
}
receiver_email = 'zpiseminar@gmail.com'  # receiver address


class MailSender():
    def __init__(self, sender, receiver_mail, measured_values):
        self._sender = sender
        self._receiver_mail = receiver_mail
        self._measured_values = measured_values

    def send_email(self, invalid_measurements):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(self._sender.mail, self._sender.password)
                server.sendmail(self._sender.mail, self._receiver_mail, self._construct_message(invalid_measurements))
                logger.info(f'sended email to {self._receiver_mail}')
        except Exception:
            logger.error('connection troubles')

    def _construct_message(self, invalid_measurements):
        message = ''
        for value in self._measured_values:
            if value in invalid_measurements:
                message += self._alert_wrong_measurement(value, invalid_measurements[value]) + '\n'

        return message[:-1]

    def _alert_wrong_measurement(self, value, measurement):
        alert = f'Wrong {value}. It is {measurement[0]} and should be {measurement[1]}.\nConsider '
        if measurement[2] == InvalidationType.LOW:
            alert += f'increasing the {value}.\n'
        else:
            alert += f'decreasing the {value}.\n'

        return alert
