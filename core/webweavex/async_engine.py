from __future__ import annotations

from .async_crawler import AsyncCrawler
from .async_fetcher import AsyncFetcher
from .config import CrawlConfig
from .js_renderer import JSRenderer
from .logging import get_logger
from .models import PageResult
from .robots import RobotsHandler

logger = get_logger(__name__)


class AsyncWebWeaveX:
  """Async entry point for concurrent crawling."""

  def __init__(
    self,
    config: CrawlConfig | None = None,
    fetcher: AsyncFetcher | None = None,
    renderer: JSRenderer | None = None,
    robots: RobotsHandler | None = None,
  ) -> None:
    self.config = config or CrawlConfig()
    self.fetcher = fetcher or AsyncFetcher(self.config)
    self._owns_fetcher = fetcher is None
    self.renderer = renderer or (JSRenderer(self.config) if self.config.enable_js else None)
    self.robots = robots or RobotsHandler(self.config)
    self._owns_robots = robots is None
    self._crawler = AsyncCrawler(
      self.fetcher,
      self.config,
      robots=self.robots,
      renderer=self.renderer,
    )
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
    if self._owns_robots:
      await self.robots.close()

  async def __aenter__(self) -> "AsyncWebWeaveX":
    return self

  async def __aexit__(self, exc_type, exc, tb) -> None:
    await self.aclose()
