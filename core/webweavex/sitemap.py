from __future__ import annotations

import xml.etree.ElementTree as ElementTree
from urllib.parse import urlparse

import httpx

from .config import CrawlConfig
from .logging import get_logger

logger = get_logger(__name__)


class SitemapDiscoverer:
  """Discover and parse sitemap URLs for crawl seeds."""

  def __init__(self, config: CrawlConfig, client: httpx.AsyncClient | None = None) -> None:
    self._config = config
    self._client = client or httpx.AsyncClient(
      timeout=config.timeout,
      headers=config.headers,
      follow_redirects=True,
    )
    self._owns_client = client is None

  async def discover(self, url: str) -> list[str]:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
      return []

    base = f"{parsed.scheme}://{parsed.netloc}"
    sitemap_urls = await self._sitemaps_from_robots(base)
    if not sitemap_urls:
      sitemap_urls = [f"{base}/sitemap.xml"]

    results: list[str] = []
    for sitemap_url in sitemap_urls:
      urls = await self._fetch_sitemap_urls(sitemap_url)
      if urls:
        logger.info("Sitemap discovered %s (%s urls)", sitemap_url, len(urls))
      results.extend(urls)

    return results

  async def _sitemaps_from_robots(self, base: str) -> list[str]:
    robots_url = f"{base}/robots.txt"
    try:
      response = await self._client.get(robots_url)
    except httpx.HTTPError:
      return []

    if response.status_code >= 400:
      return []

    sitemaps: list[str] = []
    for line in response.text.splitlines():
      if line.lower().startswith("sitemap:"):
        _, value = line.split(":", 1)
        sitemap = value.strip()
        if sitemap:
          sitemaps.append(sitemap)
    return sitemaps

  async def _fetch_sitemap_urls(self, sitemap_url: str) -> list[str]:
    try:
      response = await self._client.get(sitemap_url)
    except httpx.HTTPError:
      return []

    if response.status_code >= 400:
      return []

    urls, is_index = self._parse_sitemap_xml(response.text)
    if not is_index:
      return urls

    nested_results: list[str] = []
    for nested in urls:
      nested_results.extend(await self._fetch_sitemap_urls(nested))
    return nested_results

  def _parse_sitemap_xml(self, xml_text: str) -> tuple[list[str], bool]:
    try:
      root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
      return [], False

    tag = root.tag.lower()
    urls: list[str] = []

    if tag.endswith("sitemapindex"):
      for loc in root.findall(".//{*}loc"):
        if loc.text:
          urls.append(loc.text.strip())
      return urls, True

    if tag.endswith("urlset"):
      for loc in root.findall(".//{*}loc"):
        if loc.text:
          urls.append(loc.text.strip())
      return urls, False

    return [], False

  async def close(self) -> None:
    if self._owns_client:
      await self._client.aclose()
