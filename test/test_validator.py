from microclimate_validator import validate_climate


def test_pass_all_bad_return_false():
    assert validate_climate(temperature=27, humidity=80) is False


def test_pass_all_good_return_true():
    assert validate_climate(temperature=20, humidity=50) is True
