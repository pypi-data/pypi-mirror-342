import atexit
import logging
import time
import typing
from functools import wraps
from threading import Lock

from fspacker import config

__all__ = [
    "perf_tracker",
]


class PerformanceTracker:
    """Performance tracker class to measure the execution time of functions."""

    global_start_time = None
    function_times: typing.Dict[str, float] = {}
    total_time = 0.0
    lock = Lock()
    debug_mode = False

    @classmethod
    def initialize(cls):
        """Initialize the performance tracker."""
        if cls.global_start_time is None:
            cls.global_start_time = time.perf_counter()
            cls.function_times = {}
            cls.total_time = 0.0

            cls.debug_mode = config.get_json_config().get("mode.debug", False)

    @classmethod
    def update_total_time(cls):
        """Update the total execution time."""
        if cls.global_start_time is not None:
            cls.total_time = time.perf_counter() - cls.global_start_time

    @classmethod
    def finalize(cls):
        """Finalize the performance tracking and log the results."""
        if cls.global_start_time is not None and cls.debug_mode:
            cls.update_total_time()
            logging.debug(f"{'-' * 32}统计{'-' * 32}")
            logging.debug(f"总运行时间: [red bold]{cls.total_time:.6f}[/] s.")
            for func_name, elapsed_time in cls.function_times.items():
                percentage = (elapsed_time / cls.total_time) * 100 if cls.total_time > 0 else 0
                logging.debug(
                    f"函数 [green bold]{func_name}[/] "
                    f"调用时间: [green bold]{elapsed_time:.6f}[/]s (占比 [green bold]{percentage:.2f}%[/])."
                )
            cls.global_start_time = None


def perf_tracker(func):
    """Decorator function to test performance."""

    PerformanceTracker.initialize()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if PerformanceTracker.debug_mode:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            with PerformanceTracker.lock:
                func_name = f"{func.__module__}.{func.__name__}"
                PerformanceTracker.function_times[func_name] = (
                    PerformanceTracker.function_times.get(func_name, 0) + elapsed_time
                )

            PerformanceTracker.update_total_time()
            total_time = PerformanceTracker.total_time
            if total_time > 0:
                percentage = (elapsed_time / total_time) * 100
                logging.debug(
                    f"函数 [green bold]{func_name}[/] "
                    f"调用时间: [green bold]{elapsed_time:.6f}[/]s (占比 [green bold]{percentage:.2f}%[/])."
                )
        else:
            result = func(*args, **kwargs)

        return result

    return wrapper


atexit.register(PerformanceTracker.finalize)
