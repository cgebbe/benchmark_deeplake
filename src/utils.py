import time
from contextlib import contextmanager
from dataclasses import dataclass

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


if __name__ == "__main__":
    with measure_network_speed():
        time.sleep(5)
