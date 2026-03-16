from __future__ import annotations

from urllib.parse import urlparse

from frontier.url_frontier import URLFrontier

from ai.crawl_strategy_engine.strategy import CrawlStrategy
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
    self._strategy = CrawlStrategy(config.strategy_keywords) if config.enable_ai_strategy else None
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
      page = await process_extraction(page)
      results.append(page)
      logger.info("Page crawled %s", current_url)

      if depth >= self._config.max_depth:
        continue

      link_entries = self._extract_links(current_url, page, allowed_domains)
      for link_url, priority in link_entries:
        self._frontier.add(link_url, depth=depth + 1, priority=priority)
        logger.info("Priority assigned %s => %s", link_url, priority)
      logger.info("Links discovered %s", len(link_entries))
      logger.info("Frontier size %s", self._frontier.size())

    return results

  async def aclose(self) -> None:
    if self._owns_fetcher:
      await self._fetcher.close()
    if self._owns_robots:
      await self._robots.close()
    if self._owns_sitemap:
      await self._sitemap.close()

  def _extract_links(
    self, base_url: str, page: PageResult, allowed_domains: set[str]
  ) -> list[tuple[str, float]]:
    results: list[tuple[str, float]] = []
    for link in page.links:
      resolved = resolve_relative(base_url, link.url)
      normalized = normalize_url(resolved)
      if normalized not in self._filter_allowed([normalized], allowed_domains):
        continue
      priority = 0.0
      if self._strategy:
        priority = self._strategy.score(normalized, link.text, page.text)
      results.append((normalized, priority))

    deduped = deduplicate_urls([item[0] for item in results])
    deduped_with_priority: list[tuple[str, float]] = []
    for url in deduped:
      for link_url, priority in results:
        if link_url == url:
          deduped_with_priority.append((url, priority))
          break
    return deduped_with_priority

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
