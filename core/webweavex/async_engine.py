from __future__ import annotations

from .async_crawler import AsyncCrawler
from .async_fetcher import AsyncFetcher
from .config import CrawlConfig
from .logging import get_logger
from .models import PageResult

logger = get_logger(__name__)


class AsyncWebWeaveX:
  """Async entry point for concurrent crawling."""

  def __init__(self, config: CrawlConfig | None = None, fetcher: AsyncFetcher | None = None) -> None:
    self.config = config or CrawlConfig()
    self.fetcher = fetcher or AsyncFetcher(self.config)
    self._owns_fetcher = fetcher is None
    self._crawler = AsyncCrawler(self.fetcher, self.config)
    logger.debug("AsyncWebWeaveX engine initialized")

  async def crawl(self, url: str) -> PageResult:
    logger.info("Async engine crawl requested for %s", url)
    return await self._crawler.crawl(url)

  async def crawl_many(self, urls: list[str]) -> list[PageResult]:
    logger.info("Async engine crawl_many requested for %s urls", len(urls))
    return await self._crawler.crawl_many(urls)

  async def aclose(self) -> None:
    if self._owns_fetcher:
      await self.fetcher.close()

  async def __aenter__(self) -> "AsyncWebWeaveX":
    return self

  async def __aexit__(self, exc_type, exc, tb) -> None:
    await self.aclose()
