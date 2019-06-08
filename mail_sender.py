import smtplib
import ssl
from logger import logger
from mail_builder import MailBuilder, MailType
from config import Config

config = Config('config.json')

mtemplate = """\
Subject: Micricliate Monitor

"""


class MailSender():
    def __init__(self, sender, measured_values):
        self._sender = sender
        self._mail_builder = MailBuilder(measured_values)

    def send_alarming_email(self, invalid_measurements):
        self._send_email(self._mail_builder.build_mail(MailType.ALARM, invalid_measurements))

    def send_reminding_email(self, invalid_measurements):
        self._send_email(self._mail_builder.build_mail(MailType.REMIND, invalid_measurements))

    def send_praising_email(self):
        self._send_email(self._mail_builder.build_mail(MailType.PRAISE))

    def send_informing_mail(self, measurements):
        self._send_email(self._mail_builder.build_mail(MailType.INFO, measurements))

    def get_recivers(self):
        return config['recivers_emails']

    def _send_email(self, email_message):
        try:
            recivers = self.get_recivers()
            for reciver in recivers:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(config['smtp_server'], config['ssl_port'], context=context) as server:
                    server.login(self._sender['mail'], self._sender['password'])
                    server.sendmail(self._sender['mail'],
                                    reciver,
                                    mtemplate + email_message)
                    logger.info(f'sended email to {reciver}')
        except Exception:
            logger.exception('connection troubles')
