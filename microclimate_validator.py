import json

with open('microclimate.json') as f:
    optimal_microclimate = json.loads(f.read())


def validate_climate(temperature, humidity):
    if temperature < optimal_microclimate['temperature']['summer']['min']:
        return False
    if temperature > optimal_microclimate['temperature']['summer']['max']:
        return False
    if humidity < optimal_microclimate['humidity']['summer']['min']:
        return False
    if humidity > optimal_microclimate['humidity']['summer']['max']:
        return False
    return True
