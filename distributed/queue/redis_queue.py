from __future__ import annotations

import redis

from webweavex.logging import get_logger

logger = get_logger(__name__)


class RedisQueue:
  """Redis-backed queue using LPUSH/BRPOP."""

  def __init__(
    self,
    host: str = "localhost",
    port: int = 6379,
    name: str = "webweavex:queue",
    client: redis.Redis | None = None,
  ) -> None:
    self._name = name
    self._client = client or redis.Redis(host=host, port=port, decode_responses=True)

  def enqueue(self, url: str) -> None:
    self._client.lpush(self._name, url)

  def dequeue(self, timeout: int = 5) -> str | None:
    result = self._client.brpop(self._name, timeout=timeout)
    if result is None:
      return None
    _, url = result
    return url
