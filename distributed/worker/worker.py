from __future__ import annotations

import asyncio

from extractor.extraction_pipeline import process as process_extraction
from webweavex.async_engine import AsyncWebWeaveX
from webweavex.config import CrawlConfig
from webweavex.logging import get_logger
from webweavex.url_utils import deduplicate_urls, normalize_url, resolve_relative

from distributed.queue.redis_queue import RedisQueue

logger = get_logger(__name__)


class Worker:
  """Distributed worker that consumes URLs and crawls pages."""

  def __init__(
    self,
    config: CrawlConfig,
    queue: RedisQueue | None = None,
    engine: AsyncWebWeaveX | None = None,
  ) -> None:
    self._config = config
    self._queue = queue or RedisQueue(host=config.redis_host, port=config.redis_port)
    self._engine = engine or AsyncWebWeaveX(config)

  async def run(self) -> None:
    logger.info("Worker started %s", self._config.worker_id)
    while True:
      url = await asyncio.to_thread(self._queue.dequeue)
      if not url:
        continue
      page = await self._engine.crawl(url)
      page = process_extraction(page)
      logger.info("URL crawled %s", url)

      links = [
        normalize_url(resolve_relative(url, link.url))
        for link in page.links
      ]
      unique_links = deduplicate_urls(links)
      for link_url in unique_links:
        self._queue.enqueue(link_url)
      logger.info("Links discovered %s", len(unique_links))

  async def aclose(self) -> None:
    await self._engine.aclose()
