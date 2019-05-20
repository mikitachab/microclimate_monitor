import pytest
from config import config
from monitor import Monitor
from sensors import constants


@pytest.fixture
def monitor():
    config['test_dedicated_state'] = True
    return Monitor()


def set_all_measurements_invalid():
    constants.FAKE_SENSORS['temperature'] = 40
    constants.FAKE_SENSORS['humidity'] = 10
    constants.FAKE_SENSORS['light'] = 0
    constants.FAKE_SENSORS['is_loud'] = 1


def set_all_measurements_valid():
    constants.FAKE_SENSORS['temperature'] = 20
    constants.FAKE_SENSORS['humidity'] = 50
    constants.FAKE_SENSORS['light'] = 10
    constants.FAKE_SENSORS['is_loud'] = 0


MASUREMENTS_SETTINGS = [
    (set_all_measurements_invalid, True),
    (set_all_measurements_valid, False)
]


@pytest.mark.parametrize("set_measurements, more_frequent_measurements", MASUREMENTS_SETTINGS)
def test_increased_measurements_rate_according_to_measurement(
        set_measurements, more_frequent_measurements, monitor):
    set_measurements()
    monitor._tick()
    assert monitor._timer.increase_measurement_rate is more_frequent_measurements


@pytest.mark.parametrize("set_measurements, measurements_invalid", MASUREMENTS_SETTINGS)
def test_measurements_are_fetched_and_validated_correctly(set_measurements, measurements_invalid, monitor):
    set_measurements()
    assert monitor._receive_and_check_measurements() is not measurements_invalid


def test_average_measurements_invalid(monitor):
    set_all_measurements_invalid()
    for _ in range(config['min_measurements_count']):
        monitor._tick()
    assert len(monitor._validate_last_measurements()) is 2


def test_average_measurements_valid(monitor):
    set_all_measurements_valid()
    for _ in range(config['min_measurements_count']):
        monitor._tick()
    assert len(monitor._validate_last_measurements()) is 0


# TODO: Add mock for function calls inside monitor.py, test whether messages are sent
# def test_alarm_message_sent_when_measurements_invalid(monitor):
#     set_all_measurements_invalid()
#     for _ in range(config['min_measurements_count']):
#         monitor._tick()
#     assert
#
#
# def test_alarm_message_not_sent_when_measurements_valid(monitor):
#     set_all_measurements_valid()
#     for _ in range(config['min_measurements_count']):
#         monitor._tick()
#     assert
#
#
# def test_praise_message_not_sent_when_measurements_are_improving(monitor):
#     set_all_measurements_valid()
#     for _ in range(config['min_measurements_count']):
#         monitor._tick()
#     assert
