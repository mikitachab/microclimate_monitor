import smtplib
import ssl
from config import config
from logger import logger
from mail_builder import MailBuilder, MailType


class MailSender():
    def __init__(self, sender, receiver_mail, measured_values):
        self._sender = sender
        self._receiver_mail = receiver_mail
        self._mail_builder = MailBuilder(measured_values)

    def send_alarming_email(self, invalid_measurements):
        self._send_email(self._mail_builder.build_mail(MailType.ALARM, invalid_measurements))

    def send_reminding_email(self, invalid_measurements):
        self._send_email(self._mail_builder.build_mail(MailType.REMIND, invalid_measurements))

    def send_praising_email(self):
        self._send_email(self._mail_builder.build_mail(MailType.PRAISE))

    def send_informing_mail(self, measurements):
        self._send_email(self._mail_builder.build_mail(MailType.INFO, measurements))

    def _send_email(self, email_message):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config['smtp_server'], config['ssl_port'], context=context) as server:
                server.login(self._sender['mail'], self._sender['password'])
                server.sendmail(self._sender['mail'],
                                self._receiver_mail,
                                email_message)
                logger.info(f'sended email to {self._receiver_mail}')
        except Exception:
            logger.exception('connection troubles')
