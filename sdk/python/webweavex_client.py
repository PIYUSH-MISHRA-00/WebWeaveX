from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

import httpx

DEFAULT_RETRY_STATUSES = {408, 429, 500, 502, 503, 504}


class WebWeaveXError(Exception):
  """Base SDK error."""


class WebWeaveXTimeoutError(WebWeaveXError):
  """Raised when the request exceeds the configured timeout."""


class WebWeaveXNetworkError(WebWeaveXError):
  """Raised when a network-level error occurs."""


class WebWeaveXHTTPError(WebWeaveXError):
  """Raised for non-2xx HTTP responses."""

  def __init__(self, status_code: int, message: str, response_body: str | None = None) -> None:
    super().__init__(message)
    self.status_code = status_code
    self.response_body = response_body


@dataclass(frozen=True)
class RetryConfig:
  max_retries: int = 2
  backoff_seconds: float = 0.3
  retry_statuses: set[int] | None = None

  def __post_init__(self) -> None:
    statuses = set(DEFAULT_RETRY_STATUSES if self.retry_statuses is None else self.retry_statuses)
    object.__setattr__(self, "retry_statuses", statuses)
    object.__setattr__(self, "max_retries", max(0, self.max_retries))
    object.__setattr__(self, "backoff_seconds", max(0.0, self.backoff_seconds))

  def delay_for(self, attempt: int) -> float:
    return self.backoff_seconds * (2 ** attempt)


class WebWeaveXClient:
  def __init__(
    self,
    base_url: str,
    *,
    timeout: float = 10.0,
    max_retries: int = 2,
    backoff_seconds: float = 0.3,
    retry_statuses: set[int] | None = None,
    debug: bool = False,
    logger: Callable[[str], None] | None = None,
    client: httpx.Client | None = None,
  ) -> None:
    self.base_url = base_url.rstrip("/")
    self.debug = debug
    self._logger = logger or print
    self.retry = RetryConfig(
      max_retries=max_retries,
      backoff_seconds=backoff_seconds,
      retry_statuses=retry_statuses,
    )
    self._owns_client = client is None
    self._client = client or httpx.Client(
      timeout=timeout,
      headers={"Content-Type": "application/json"},
    )

  def crawl(self, url: str) -> dict[str, Any]:
    return self._post("/crawl", {"url": url})

  def crawl_site(self, url: str) -> list[dict[str, Any]]:
    return self._post("/crawl_site", {"url": url})

  def crawlSite(self, url: str) -> list[dict[str, Any]]:
    return self.crawl_site(url)

  def rag_dataset(self, url: str) -> list[dict[str, Any]]:
    return self._post("/rag_dataset", {"url": url})

  def ragDataset(self, url: str) -> list[dict[str, Any]]:
    return self.rag_dataset(url)

  def knowledge_graph(self, url: str) -> dict[str, list[dict[str, str]]]:
    return self._post("/knowledge_graph", {"url": url})

  def knowledgeGraph(self, url: str) -> dict[str, list[dict[str, str]]]:
    return self.knowledge_graph(url)

  def _post(self, path: str, payload: dict[str, Any]) -> Any:
    url = f"{self.base_url}{path}"
    last_error: Exception | None = None

    for attempt in range(self.retry.max_retries + 1):
      attempt_no = attempt + 1
      self._log(f"POST {url} attempt {attempt_no}/{self.retry.max_retries + 1}")
      try:
        response = self._client.post(url, json=payload)
        if response.status_code in self.retry.retry_statuses and attempt < self.retry.max_retries:
          self._log(
            f"HTTP {response.status_code} for {url}; retrying in {self.retry.delay_for(attempt):.2f}s"
          )
          time.sleep(self.retry.delay_for(attempt))
          continue
        response.raise_for_status()
        self._log(f"POST {url} succeeded with HTTP {response.status_code}")
        return response.json()
      except httpx.TimeoutException:
        last_error = WebWeaveXTimeoutError(
          f"Request timed out after {self._client.timeout} for {url} "
          f"(attempt {attempt_no}/{self.retry.max_retries + 1})"
        )
      except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status in self.retry.retry_statuses and attempt < self.retry.max_retries:
          self._log(f"Retryable HTTP {status} for {url}; retrying in {self.retry.delay_for(attempt):.2f}s")
          time.sleep(self.retry.delay_for(attempt))
          continue
        message = (
          f"Request failed with HTTP {status} for {url} "
          f"(attempt {attempt_no}/{self.retry.max_retries + 1})"
        )
        last_error = WebWeaveXHTTPError(status, message, exc.response.text)
      except httpx.RequestError as exc:
        last_error = WebWeaveXNetworkError(
          f"Network request failed for {url} "
          f"(attempt {attempt_no}/{self.retry.max_retries + 1}): {exc}"
        )
      except ValueError as exc:
        raise WebWeaveXError(f"Invalid JSON response from {url}: {exc}") from exc

      if attempt < self.retry.max_retries:
        self._log(f"{last_error}. Retrying in {self.retry.delay_for(attempt):.2f}s")
        time.sleep(self.retry.delay_for(attempt))
        continue
      if last_error:
        self._log(f"POST {url} failed after retries: {last_error}")
        raise last_error
      raise WebWeaveXError(f"Request failed for {url}")

    raise WebWeaveXError(f"Request failed for {url}")

  def close(self) -> None:
    if self._owns_client:
      self._client.close()

  def __enter__(self) -> "WebWeaveXClient":
    return self

  def __exit__(self, exc_type, exc, tb) -> None:
    self.close()

  def _log(self, message: str) -> None:
    if self.debug:
      self._logger(f"[WebWeaveX SDK] {message}")
