import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from pynteracta.exceptions import InteractaResponseError


def retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except InteractaResponseError:
                    if retries == max_retries - 1:
                        raise
                    retries += 1
                    time.sleep(delay)
            return None

        return wrapper

    return decorator
