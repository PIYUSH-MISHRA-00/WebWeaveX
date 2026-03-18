from __future__ import annotations

import time

import httpx

from .config import CrawlConfig
from .exceptions import FetchError
from .logging import get_logger
from .rate_limiter import RateLimiter
from .ssl_utils import get_ssl_verify

logger = get_logger(__name__)


class HttpFetcher:
  """Simple HTTP fetcher with retry support."""

  def __init__(self, config: CrawlConfig, client: httpx.Client | None = None) -> None:
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

    self._client = client or httpx.Client(
      timeout=timeout,
      headers=config.headers,
      follow_redirects=True,
      verify=verify,
    )
    self._owns_client = client is None

  def fetch(self, url: str) -> tuple[int, str]:
    last_exc: Exception | None = None
    attempts = max(self._config.retries, 0) + 1
    backoff = self._config.retry_backoff_base
    for attempt in range(1, attempts + 1):
      try:
        self._rate_limiter.acquire()
        logger.info("Fetching %s", url)
        response = self._client.get(url)
        return response.status_code, response.text
      except httpx.HTTPError as exc:
        logger.warning("Fetch attempt %s failed for %s: %s", attempt, url, exc)
        last_exc = exc
        if attempt < attempts:
          sleep_for = min(backoff, self._config.retry_backoff_max)
          time.sleep(sleep_for)
          backoff *= 2
    raise FetchError(f"Failed to fetch {url}") from last_exc

  def close(self) -> None:
    if self._owns_client:
      self._client.close()

  def __enter__(self) -> "HttpFetcher":
    return self

  def __exit__(self, exc_type, exc, tb) -> None:
    self.close()
