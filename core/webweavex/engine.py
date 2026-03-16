from __future__ import annotations

from .config import CrawlConfig
from .crawler import Crawler
from .fetcher import HttpFetcher
from .logging import get_logger
from .models import PageResult

logger = get_logger(__name__)

class WebWeaveX:
  """Public entry point for the core engine."""

  def __init__(self, config: CrawlConfig | None = None, fetcher: HttpFetcher | None = None) -> None:
    self.config = config or CrawlConfig()
    self.fetcher = fetcher or HttpFetcher(self.config)
    self._crawler = Crawler(self.fetcher, self.config)
    logger.debug("WebWeaveX engine initialized")

  def crawl(self, url: str) -> PageResult:
    """Fetch and parse a single URL."""
    logger.info("Engine crawl requested for %s", url)
    return self._crawler.crawl(url)
