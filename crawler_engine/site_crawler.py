from __future__ import annotations

from urllib.parse import urlparse

from frontier.url_frontier import URLFrontier

from webweavex.async_crawler import AsyncCrawler
from webweavex.async_fetcher import AsyncFetcher
from webweavex.config import CrawlConfig
from webweavex.js_renderer import JSRenderer
from webweavex.logging import get_logger
from webweavex.models import PageResult
from webweavex.robots import RobotsHandler
from webweavex.sitemap import SitemapDiscoverer
from webweavex.url_utils import deduplicate_urls, normalize_url, resolve_relative
from extractor.extraction_pipeline import process as process_extraction

logger = get_logger(__name__)


class SiteCrawler:
  """Crawl multiple pages within a site starting from a seed URL."""

  def __init__(
    self,
    config: CrawlConfig,
    fetcher: AsyncFetcher | None = None,
    robots: RobotsHandler | None = None,
    renderer: JSRenderer | None = None,
    sitemap: SitemapDiscoverer | None = None,
    frontier: URLFrontier | None = None,
  ) -> None:
    self._config = config
    self._fetcher = fetcher or AsyncFetcher(config)
    self._owns_fetcher = fetcher is None
    self._robots = robots or RobotsHandler(config)
    self._owns_robots = robots is None
    self._renderer = renderer or (JSRenderer(config) if config.enable_js else None)
    self._sitemap = sitemap or SitemapDiscoverer(config)
    self._owns_sitemap = sitemap is None
    self._frontier = frontier or URLFrontier(max_depth=config.max_depth)
    self._crawler = AsyncCrawler(
      self._fetcher,
      config,
      robots=self._robots,
      renderer=self._renderer,
    )

  async def crawl_site(self, url: str) -> list[PageResult]:
    seed = normalize_url(url)
    logger.info("Site crawl started for %s", seed)

    allowed_domains = self._resolve_allowed_domains(seed)
    self._frontier.add(seed, depth=0)

    sitemap_urls = await self._sitemap.discover(seed)
    sitemap_urls = self._filter_allowed(sitemap_urls, allowed_domains)
    self._frontier.add_many(sitemap_urls, depth=0)

    results: list[PageResult] = []
    while len(results) < self._config.max_pages:
      next_item = self._frontier.next()
      if not next_item:
        break
      current_url, depth = next_item
      page = await self._crawler.crawl(current_url)
      page = process_extraction(page)
      results.append(page)
      logger.info("Page crawled %s", current_url)

      if depth >= self._config.max_depth:
        continue

      link_urls = self._extract_links(current_url, page, allowed_domains)
      self._frontier.add_many(link_urls, depth=depth + 1)
      logger.info("Links discovered %s", len(link_urls))
      logger.info("Frontier size %s", self._frontier.size())

    return results

  async def aclose(self) -> None:
    if self._owns_fetcher:
      await self._fetcher.close()
    if self._owns_robots:
      await self._robots.close()
    if self._owns_sitemap:
      await self._sitemap.close()

  def _extract_links(self, base_url: str, page: PageResult, allowed_domains: set[str]) -> list[str]:
    raw_links = [link.url for link in page.links]
    resolved = [resolve_relative(base_url, link) for link in raw_links]
    normalized = [normalize_url(link) for link in resolved]
    filtered = self._filter_allowed(normalized, allowed_domains)
    return deduplicate_urls(filtered)

  def _resolve_allowed_domains(self, seed: str) -> set[str]:
    if self._config.allowed_domains:
      allowed: set[str] = set()
      for domain in self._config.allowed_domains:
        parsed = urlparse(domain)
        host = parsed.netloc or parsed.path
        if host:
          allowed.add(host.lower())
      return allowed

    parsed = urlparse(seed)
    if parsed.netloc:
      return {parsed.netloc.lower()}
    return set()

  def _filter_allowed(self, urls: list[str], allowed_domains: set[str]) -> list[str]:
    if not allowed_domains:
      return urls

    results: list[str] = []
    for url in urls:
      parsed = urlparse(url)
      netloc = parsed.netloc.lower()
      if not netloc:
        continue
      if netloc in allowed_domains:
        results.append(url)
        continue
      for domain in allowed_domains:
        if netloc.endswith(f".{domain}"):
          results.append(url)
          break
    return results
