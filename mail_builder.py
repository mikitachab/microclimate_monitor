from enum import Enum
from microclimate_validator import InvalidationType


class MailSystemException(Exception):
    pass


class MailType(Enum):
    ALARM = 0
    REMIND = 1
    PRAISE = 2
    INFO = 3


class MailBuilder():
    def __init__(self, measured_values):
        self._measured_values = measured_values

    def build_mail(self, mail_type, measurements=None):
        if mail_type == MailType.PRAISE:
            return self._construct_praising_mail()
        elif mail_type == MailType.INFO:
            return self._construct_informing_mail(measurements)
        elif mail_type == MailType.REMIND:
            return self._construct_reminding_mail(measurements)
        elif mail_type == MailType.ALARM:
            return self._construct_alarming_mail(measurements)
        else:
            raise MailSystemException(
                'Unknown type of mail requested to build')

    def _construct_praising_mail(self):
        return 'Everything is good with your climate now!\n'

    def _construct_informing_mail(self, measurements):
        if not measurements:
            raise MailSystemException(
                'Informing mail should know about current state of climate')

        mail = 'Daily message from microclimate monitor. Current climate:\n'
        for value in self._measured_values:
            mail += f'{value}: {measurements[value]}\n'

        return mail

    def _construct_reminding_mail(self, measurements):
        if not measurements:
            raise MailSystemException(
                'Reminding mail should know about current state of climate')

        return 'Last problems are still not fixed! Reminder: \n' + self._construct_message(measurements)

    def _construct_alarming_mail(self, measurements):
        if not measurements:
            raise MailSystemException(
                'Alarming mail should know about current state of climate')

        return 'A problem occured with your climate!\n' + self._construct_message(measurements)

    def _construct_message(self, invalid_measurements):
        message = ''
        for value in self._measured_values:
            if value in invalid_measurements:
                message += self._alert_wrong_measurement(
                    value, invalid_measurements[value]) + '\n'

        return message[:-1]

    def _alert_wrong_measurement(self, value, measurement):
        alert = f'Wrong {value}. It is {measurement[0]} and should be {measurement[1]}.\nConsider '
        if measurement[2] == InvalidationType.LOW:
            alert += f'increasing the {value}.\n'
        else:
            alert += f'decreasing the {value}.\n'

        return alert
