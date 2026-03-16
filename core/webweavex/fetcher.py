from __future__ import annotations

import httpx

from .config import CrawlConfig
from .exceptions import FetchError


class HttpFetcher:
  """Simple HTTP fetcher with retry support."""

  def __init__(self, config: CrawlConfig, client: httpx.Client | None = None) -> None:
    self._config = config
    self._client = client or httpx.Client(
      timeout=config.timeout,
      headers=config.headers,
      follow_redirects=True,
    )
    self._owns_client = client is None

  def fetch(self, url: str) -> tuple[int, str]:
    last_exc: Exception | None = None
    attempts = max(self._config.retries, 0) + 1
    for _ in range(attempts):
      try:
        response = self._client.get(url)
        return response.status_code, response.text
      except httpx.HTTPError as exc:
        last_exc = exc
    raise FetchError(f"Failed to fetch {url}") from last_exc

  def close(self) -> None:
    if self._owns_client:
      self._client.close()

  def __enter__(self) -> "HttpFetcher":
    return self

  def __exit__(self, exc_type, exc, tb) -> None:
    self.close()
