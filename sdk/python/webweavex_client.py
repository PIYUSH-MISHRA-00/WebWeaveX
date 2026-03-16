from __future__ import annotations

import httpx


class WebWeaveXClient:
  """Python SDK client for the WebWeaveX API."""

  def __init__(self, base_url: str, timeout: float = 10.0) -> None:
    self._base_url = base_url.rstrip("/")
    self._client = httpx.Client(timeout=timeout)

  def crawl(self, url: str) -> dict[str, object]:
    return self._post("/crawl", {"url": url})

  def crawl_site(self, url: str) -> list[dict[str, object]]:
    return self._post("/crawl_site", {"url": url})

  def rag_dataset(self, url: str) -> list[dict[str, object]]:
    return self._post("/rag_dataset", {"url": url})

  def knowledge_graph(self, url: str) -> dict[str, object]:
    return self._post("/knowledge_graph", {"url": url})

  def _post(self, path: str, payload: dict[str, object]) -> object:
    response = self._client.post(f"{self._base_url}{path}", json=payload)
    response.raise_for_status()
    return response.json()

  def close(self) -> None:
    self._client.close()

  def __enter__(self) -> "WebWeaveXClient":
    return self

  def __exit__(self, exc_type, exc, tb) -> None:
    self.close()
