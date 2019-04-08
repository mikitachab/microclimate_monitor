from enum import Enum
import json


class InvalidationType(Enum):
    LOW = 0
    HIGH = 1


with open('microclimate.json') as f:
    optimal_microclimate = json.loads(f.read())


def validate_climate(temperature, humidity):
    invalid_measurements = {}
    if temperature < optimal_microclimate['temperature']['summer']['min']:
        invalid_measurements['temperature'] = (temperature, InvalidationType.LOW)
    if temperature > optimal_microclimate['temperature']['summer']['max']:
        invalid_measurements['temperature'] = (temperature, InvalidationType.HIGH)
    if humidity < optimal_microclimate['humidity']['summer']['min']:
        invalid_measurements['humidity'] = (humidity, InvalidationType.LOW)
    if humidity > optimal_microclimate['humidity']['summer']['max']:
        invalid_measurements['humidity'] = (humidity, InvalidationType.HIGH)

    return invalid_measurements
