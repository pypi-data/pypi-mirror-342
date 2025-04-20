"""Contains global fixtures for unit tests."""

import time

import pytest


@pytest.fixture
def timer_1_second():
    """Sleep for 1 second."""

    def inner():
        time.sleep(1)

    return inner


@pytest.fixture
def error():
    """Raise an error."""

    def inner():
        msg = "Lorem Ipsum"
        raise OSError(msg)

    return inner
