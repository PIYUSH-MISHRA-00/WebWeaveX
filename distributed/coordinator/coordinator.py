from __future__ import annotations

from webweavex.config import CrawlConfig
from webweavex.logging import get_logger
from webweavex.sitemap import SitemapDiscoverer
from webweavex.url_utils import deduplicate_urls, normalize_url

from distributed.queue.redis_queue import RedisQueue

logger = get_logger(__name__)


class Coordinator:
  """Coordinator that seeds the distributed crawl queue."""

  def __init__(
    self,
    config: CrawlConfig,
    queue: RedisQueue | None = None,
    sitemap: SitemapDiscoverer | None = None,
  ) -> None:
    self._config = config
    self._queue = queue or RedisQueue(host=config.redis_host, port=config.redis_port)
    self._sitemap = sitemap or SitemapDiscoverer(config)
    self._owns_sitemap = sitemap is None

  async def start_crawl(self, seed_url: str) -> None:
    seed = normalize_url(seed_url)
    logger.info("Coordinator seeding %s", seed)
    self._queue.enqueue(seed)

    urls = await self._sitemap.discover(seed)
    for url in deduplicate_urls(urls):
      self._queue.enqueue(url)
      logger.info("Coordinator enqueued %s", url)

  async def aclose(self) -> None:
    if self._owns_sitemap:
      await self._sitemap.close()
