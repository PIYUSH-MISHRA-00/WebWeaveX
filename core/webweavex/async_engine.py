from __future__ import annotations

from .config import CrawlConfig


class AsyncWebWeaveX:
  """Async engine interface (implementation scheduled for Phase 2)."""

  def __init__(self, config: CrawlConfig | None = None) -> None:
    self.config = config or CrawlConfig()

  async def crawl(self, url: str):
    """Async crawl stub to be implemented in Phase 2."""
    raise NotImplementedError("Async crawling will be implemented in Phase 2")
