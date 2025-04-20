"""Stub unit test file."""

import logging
import threading

import pytest
from pytest_mock import MockerFixture

from extended_functools.timeout import timeout


def test_timeout_no_error(timer_1_second):
    """Test the timeout decorator's happy path."""
    assert timeout(timeout=2)(timer_1_second)() is None


def test_timeout_raise_error(timer_1_second):
    """Test the timeout decorator raises an exception."""
    with pytest.raises(TimeoutError, match=rf"function \[{timer_1_second.__name__}\]"):
        timeout(timeout=0)(timer_1_second)()


def test_timeout_raise_consecutive_errors(timer_1_second):
    """Test the timeout decorator raises exceptions reliably."""
    for _ in range(5):
        with pytest.raises(TimeoutError, match=rf"function \[{timer_1_second.__name__}\]"):
            timeout(timeout=0)(timer_1_second)()


def test_timeout_raise_error_from_decorated_function(error):
    """Test the timeout decorator propagates errors correctly."""
    with pytest.raises(OSError, match="Lorem Ipsum"):
        timeout(timeout=5)(error)()


def test_timeout_threading_error(caplog: pytest.LogCaptureFixture, mocker: MockerFixture, timer_1_second):
    """Test having an error creating threads."""
    mocker.patch.object(threading.Thread, threading.Thread.start.__name__, side_effect=ValueError("Hello"))
    with pytest.raises(ValueError, match="Hello"):
        timeout(timeout=5)(timer_1_second)()
    assert caplog.at_level(logging.ERROR)
    assert caplog.messages[-1] == "Error starting thread"
