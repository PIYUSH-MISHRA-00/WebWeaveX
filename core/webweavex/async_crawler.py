from __future__ import annotations

import asyncio

from .async_fetcher import AsyncFetcher
from .config import CrawlConfig
from .crawler import parse_html
from .logging import get_logger
from .models import PageResult

logger = get_logger(__name__)


class AsyncCrawler:
  """Concurrent async crawler for multiple URLs."""

  def __init__(self, fetcher: AsyncFetcher, config: CrawlConfig) -> None:
    self._fetcher = fetcher
    self._config = config
    self._semaphore = asyncio.Semaphore(max(1, config.max_concurrency))

  async def crawl(self, url: str) -> PageResult:
    logger.info("Async crawling %s", url)
    async with self._semaphore:
      status, html = await self._fetcher.fetch(url)
    links, metadata = parse_html(html)
    return PageResult(url=url, status=status, html=html, links=links, metadata=metadata)

  async def crawl_many(self, urls: list[str]) -> list[PageResult]:
    tasks = [asyncio.create_task(self.crawl(url)) for url in urls]
    return await asyncio.gather(*tasks)
