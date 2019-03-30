import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
dht11_instance = dht11.DHT11(pin=17)


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
