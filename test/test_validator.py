from ... import microclimate_validator


def test_validator_return_true():
    assert validate_climate(temperature=20, humidity=50) == True


def test_validator_return_false():
    assert validate_climate(temperature=27, humidity=80) == False


def test_validator_normal_humidity_return_false():
    assert validate_climate(temperature=27, humidity=50) == False
