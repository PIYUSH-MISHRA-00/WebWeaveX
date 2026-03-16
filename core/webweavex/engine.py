from __future__ import annotations

from .config import CrawlConfig
from .crawler import Crawler
from .fetcher import HttpFetcher
from .models import PageResult


class WebWeaveX:
  """Public entry point for the core engine."""

  def __init__(self, config: CrawlConfig | None = None, fetcher: HttpFetcher | None = None) -> None:
    self.config = config or CrawlConfig()
    self.fetcher = fetcher or HttpFetcher(self.config)
    self._crawler = Crawler(self.fetcher, self.config)

  def crawl(self, url: str) -> PageResult:
    """Fetch and parse a single URL."""
    return self._crawler.crawl(url)
