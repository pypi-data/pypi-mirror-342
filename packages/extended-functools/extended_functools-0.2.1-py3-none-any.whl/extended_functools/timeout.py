"""Timeout functions."""

from __future__ import annotations

import functools
import logging
from threading import Thread
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)

T = TypeVar("T")


def timeout(timeout: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Raise an exception if the decorated function is too slow to execute."""

    def deco(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:  # noqa: ANN401
            result: T | Exception = TimeoutError(f"function [{func.__name__}] timeout [{timeout} seconds] exceeded!")

            def process() -> None:
                nonlocal result
                try:
                    result = func(*args, **kwargs)
                except Exception as err:  # noqa: BLE001
                    result = err

            t = Thread(target=process, daemon=True)
            try:
                t.start()
                t.join(timeout=timeout)
            except Exception:
                logger.exception("Error starting thread")
                raise
            if isinstance(result, BaseException):
                raise result
            return result

        return wrapper

    return deco
