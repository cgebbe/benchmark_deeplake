import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pprint import pprint

import numpy as np
import psutil


@dataclass
class _NetworkSnapshot:
    time: float
    byte_count: int


def _take_snapshot():
    return _NetworkSnapshot(
        time=time.time(),
        byte_count=psutil.net_io_counters().bytes_recv,
    )


@contextmanager
def measure_network_speed():
    start = _take_snapshot()
    try:
        yield
    finally:
        stop = _take_snapshot()
        elapsed_time = stop.time - start.time
        total_bytes = stop.byte_count - start.byte_count
        speed = total_bytes / elapsed_time / 1e6
        print(f"Average network download speed of {speed:.3f} MB/s")


def check_env_vars():
    required_env_keys = {
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
        "S3_BUCKET_NAME",
        "S3_PREFIX",
    }
    missing_keys = required_env_keys.difference(os.environ)
    if missing_keys:
        raise ValueError(f"Please provide {missing_keys=}")


class StopWatch:
    def __init__(self):
        self.durations = []
        self.last_time = None
        self.start()

    def start(self):
        self.last_time = time.time()

    def stop(self):
        now_time = time.time()
        self.durations.append(now_time - self.last_time)
        self.last_time = now_time

    def evaluate(self):
        self.durations.sort()
        iterations_per_second = {
            f"fastest_{x:03d}%": 1
            / np.mean(self.durations[0 : int(x / 100 * len(self.durations))])
            for x in [50, 80, 90, 95, 98, 99, 100]
        }
        pprint(iterations_per_second)
