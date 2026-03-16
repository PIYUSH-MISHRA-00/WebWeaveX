from __future__ import annotations

import asyncio
import threading
import time


class RateLimiter:
  """Simple rate limiter using a fixed interval between requests."""

  def __init__(self, rate_per_second: float) -> None:
    self._interval = 1.0 / rate_per_second if rate_per_second and rate_per_second > 0 else 0.0
    self._last_called = 0.0
    self._lock = threading.Lock()
    self._async_lock = asyncio.Lock()

  def acquire(self) -> None:
    if self._interval <= 0:
      return
    with self._lock:
      now = time.monotonic()
      wait_time = self._interval - (now - self._last_called)
      if wait_time > 0:
        time.sleep(wait_time)
      self._last_called = time.monotonic()

  async def acquire_async(self) -> None:
    if self._interval <= 0:
      return
    async with self._async_lock:
      now = time.monotonic()
      wait_time = self._interval - (now - self._last_called)
      if wait_time > 0:
        await asyncio.sleep(wait_time)
      self._last_called = time.monotonic()
