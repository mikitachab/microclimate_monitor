import smtplib
import ssl
from logger import logger

port = 465  # for SSL
smtp_server = 'smtp.gmail.com'
pi_sender_email = 'microclimatepi@gmail.com'  # raspberry pi email address
test_receiver_email = 'zpiseminar@gmail.com'  # receiver address

with open('.secret') as f:
    password = f.read()


test_message = """\
Subject: Hi there

This message is sent from Python.
Rasberry Pi started monitoring.
"""


def send_email(receiver, message):
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(pi_sender_email, password)
            server.sendmail(pi_sender_email, receiver, message)
            logger.info(f'sended email to {receiver}')
    except Exception:
        logger.error('connection troubles')


if __name__ == '__main__':
    send_email(receiver=test_receiver_email, message=test_message)
