from __future__ import annotations

import asyncio

from .async_fetcher import AsyncFetcher
from .config import CrawlConfig
from .crawler import parse_html
from .js_renderer import JSRenderer
from .logging import get_logger
from .models import Metadata, PageResult
from .robots import RobotsHandler

logger = get_logger(__name__)


class AsyncCrawler:
  """Concurrent async crawler for multiple URLs."""

  def __init__(
    self,
    fetcher: AsyncFetcher,
    config: CrawlConfig,
    robots: RobotsHandler | None = None,
    renderer: JSRenderer | None = None,
  ) -> None:
    self._fetcher = fetcher
    self._config = config
    self._robots = robots
    self._renderer = renderer
    self._semaphore = asyncio.Semaphore(max(1, config.max_concurrency))

  async def crawl(self, url: str) -> PageResult:
    logger.info("Async crawling %s", url)
    if self._robots:
      allowed = await self._robots.allowed(url)
      if not allowed:
        logger.info("Robots blocked %s", url)
        return PageResult(url=url, status=403, html=None, links=[], metadata=Metadata())

    async with self._semaphore:
      if self._config.enable_js:
        if self._renderer is None:
          logger.warning("JS rendering enabled but no renderer configured; falling back to fetcher")
          status, html = await self._fetcher.fetch(url)
        else:
          logger.info("JS rendering used for %s", url)
          html = await self._renderer.render(url)
          status = 200
      else:
        status, html = await self._fetcher.fetch(url)
    links, metadata = parse_html(html)
    return PageResult(url=url, status=status, html=html, links=links, metadata=metadata)

  async def crawl_many(self, urls: list[str]) -> list[PageResult]:
    tasks = [asyncio.create_task(self.crawl(url)) for url in urls]
    return await asyncio.gather(*tasks)
