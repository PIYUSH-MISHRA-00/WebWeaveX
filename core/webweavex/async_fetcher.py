from __future__ import annotations

import asyncio

import httpx

from .config import CrawlConfig
from .exceptions import FetchError
from .logging import get_logger
from .rate_limiter import RateLimiter
from .ssl_utils import get_ssl_verify

logger = get_logger(__name__)


class AsyncFetcher:
  """Async HTTP fetcher with retry and backoff."""

  def __init__(self, config: CrawlConfig, client: httpx.AsyncClient | None = None) -> None:
    self._config = config
    self._rate_limiter = RateLimiter(config.rate_limit_per_second)
    timeout = httpx.Timeout(
      config.timeout,
      connect=config.connect_timeout,
      read=config.read_timeout,
      write=config.write_timeout,
      pool=config.pool_timeout,
    )
    
    verify = get_ssl_verify(config.ssl_verify)

    self._client = client or httpx.AsyncClient(
      timeout=timeout,
      headers=config.headers,
      follow_redirects=True,
      verify=verify,
    )
    self._owns_client = client is None

  async def fetch(self, url: str) -> tuple[int, str]:
    last_exc: Exception | None = None
    attempts = max(self._config.retries, 0) + 1
    backoff = self._config.retry_backoff_base

    for attempt in range(1, attempts + 1):
      try:
        await self._rate_limiter.acquire_async()
        logger.info("Async fetching %s", url)
        response = await self._client.get(url)
        return response.status_code, response.text
      except httpx.HTTPError as exc:
        last_exc = exc
        logger.warning("Async fetch attempt %s failed for %s: %s", attempt, url, exc)
        if attempt < attempts:
          sleep_for = min(backoff, self._config.retry_backoff_max)
          await asyncio.sleep(sleep_for)
          backoff *= 2

    raise FetchError(f"Failed to fetch {url}") from last_exc

  async def close(self) -> None:
    if self._owns_client:
      await self._client.aclose()

  async def __aenter__(self) -> "AsyncFetcher":
    return self

  async def __aexit__(self, exc_type, exc, tb) -> None:
    await self.close()
