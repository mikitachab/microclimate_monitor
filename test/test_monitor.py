import pytest

from monitor import Monitor


@pytest.fixture
def monitor():
    return Monitor()


def test_dummy(monitor):
    assert monitor is not None
