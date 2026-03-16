import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from crawler_engine.site_crawler import SiteCrawler
from webweavex.config import CrawlConfig


class MappingAsyncFetcher:
  def __init__(self, pages: dict[str, str]) -> None:
    self._pages = pages
    self.calls: list[str] = []

  async def fetch(self, url: str):
    self.calls.append(url)
    if url not in self._pages:
      raise AssertionError(f"Unexpected URL fetched: {url}")
    return 200, self._pages[url]


class AllowAllRobots:
  async def allowed(self, url: str) -> bool:
    return True


class FakeSitemapDiscoverer:
  def __init__(self, urls: list[str]) -> None:
    self._urls = urls

  async def discover(self, url: str) -> list[str]:
    return self._urls

  async def close(self) -> None:
    return None


class SiteCrawlerTests(unittest.IsolatedAsyncioTestCase):
  async def test_crawl_site_small(self):
    pages = {
      "https://example.com/": "<a href='/a'>A</a><a href='https://example.com/b'>B</a>",
      "https://example.com/a": "<a href='/b'>B</a><a href='/a'>A</a>",
      "https://example.com/b": "<html><head><title>B</title></head></html>",
      "https://example.com/sitemap": "<html><head><title>S</title></head></html>",
    }
    fetcher = MappingAsyncFetcher(pages)
    sitemap = FakeSitemapDiscoverer(["https://example.com/sitemap"])
    config = CrawlConfig(max_pages=10, max_depth=2)

    crawler = SiteCrawler(
      config,
      fetcher=fetcher,
      robots=AllowAllRobots(),
      sitemap=sitemap,
    )

    results = await crawler.crawl_site("https://example.com/")

    crawled_urls = {result.url for result in results}
    self.assertEqual(crawled_urls, set(pages.keys()))
    self.assertEqual(fetcher.calls.count("https://example.com/b"), 1)

  async def test_depth_limit(self):
    pages = {
      "https://example.com/": "<a href='/child'>Child</a>",
      "https://example.com/child": "<a href='/grandchild'>Grand</a>",
      "https://example.com/grandchild": "<html></html>",
    }
    fetcher = MappingAsyncFetcher(pages)
    config = CrawlConfig(max_pages=10, max_depth=1)

    crawler = SiteCrawler(
      config,
      fetcher=fetcher,
      robots=AllowAllRobots(),
      sitemap=FakeSitemapDiscoverer([]),
    )

    results = await crawler.crawl_site("https://example.com/")
    crawled_urls = {result.url for result in results}
    self.assertIn("https://example.com/", crawled_urls)
    self.assertIn("https://example.com/child", crawled_urls)
    self.assertNotIn("https://example.com/grandchild", crawled_urls)

  async def test_max_pages_limit(self):
    pages = {
      "https://example.com/": "<a href='/1'>1</a><a href='/2'>2</a><a href='/3'>3</a>",
      "https://example.com/1": "<html></html>",
      "https://example.com/2": "<html></html>",
      "https://example.com/3": "<html></html>",
    }
    fetcher = MappingAsyncFetcher(pages)
    config = CrawlConfig(max_pages=2, max_depth=2)

    crawler = SiteCrawler(
      config,
      fetcher=fetcher,
      robots=AllowAllRobots(),
      sitemap=FakeSitemapDiscoverer([]),
    )

    results = await crawler.crawl_site("https://example.com/")
    self.assertEqual(len(results), 2)


if __name__ == "__main__":
  unittest.main()
