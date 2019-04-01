from microclimate_validator import validate_climate


def test_validator_return_true():
    assert validate_climate(temperature=20, humidity=50) == True


def test_validator_return_false():
    assert validate_climate(temperature=27, humidity=80) == False
