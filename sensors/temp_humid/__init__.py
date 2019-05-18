from sensors.constants import IMPORT_RASPBIAN_ONLY_PACKAGES


class DHT11Fake():
    def __init__(self, fake_read):
        self._fake_read = fake_read

    def read(self):
        return self._fake_read


if IMPORT_RASPBIAN_ONLY_PACKAGES:
    import sensors.temp_humid.dht11 as dht11
    import RPi.GPIO as GPIO

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # read data using pin 17
    dht11_instance = dht11.DHT11(pin=17)
else:
    from sensors.constants import FAKE_DHT11_READ

    dht11_instance = DHT11Fake(FAKE_DHT11_READ)


def get_temperature():
    while True:
        result = dht11_instance.read()
        if result.is_valid():
            break
    return result.temperature


def get_humidity():
    while True:
        result = dht11_instance.read()
        if result.is_valid():
            break
    return result.humidity


def get_temperature_and_humidity():
    while True:
        result = dht11_instance.read()
        if result.is_valid():
            break
    return result.temperature, result.humidity
