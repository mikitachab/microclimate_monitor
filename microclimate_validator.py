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
        invalid_measurements['temperature'] = (
            temperature, optimal_microclimate['temperature']['summer']['min'], InvalidationType.LOW)
    if temperature > optimal_microclimate['temperature']['summer']['max']:
        invalid_measurements['temperature'] = (
            temperature, optimal_microclimate['temperature']['summer']['max'], InvalidationType.HIGH)
    if humidity < optimal_microclimate['humidity']['summer']['min']:
        invalid_measurements['humidity'] = (
            humidity, optimal_microclimate['humidity']['summer']['min'], InvalidationType.LOW)
    if humidity > optimal_microclimate['humidity']['summer']['max']:
        invalid_measurements['humidity'] = (
            humidity, optimal_microclimate['humidity']['summer']['max'], InvalidationType.HIGH)

    return invalid_measurements
