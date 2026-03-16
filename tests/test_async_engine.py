import asyncio
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from webweavex.async_crawler import AsyncCrawler
from webweavex.async_engine import AsyncWebWeaveX
from webweavex.config import CrawlConfig


class DummyAsyncFetcher:
  def __init__(self, html: str, status: int = 200) -> None:
    self._html = html
    self._status = status

  async def fetch(self, url: str):
    return self._status, self._html


class MappingAsyncFetcher:
  def __init__(self, pages: dict[str, str]) -> None:
    self._pages = pages

  async def fetch(self, url: str):
    return 200, self._pages[url]


class ConcurrencyFetcher:
  def __init__(self, delay: float = 0.05) -> None:
    self._delay = delay
    self.active = 0
    self.max_active = 0
    self._lock = asyncio.Lock()

  async def fetch(self, url: str):
    async with self._lock:
      self.active += 1
      if self.active > self.max_active:
        self.max_active = self.active
    await asyncio.sleep(self._delay)
    async with self._lock:
      self.active -= 1
    return 200, "<html></html>"


class AsyncEngineTests(unittest.IsolatedAsyncioTestCase):
  async def test_async_crawl_single(self):
    html = """
    <html>
      <head><title>Async Page</title></head>
      <body><a href="/a">A</a></body>
    </html>
    """
    engine = AsyncWebWeaveX(fetcher=DummyAsyncFetcher(html))
    result = await engine.crawl("https://example.com")
    self.assertEqual(result.url, "https://example.com")
    self.assertEqual(result.status, 200)
    self.assertEqual(result.metadata.title, "Async Page")
    self.assertEqual(len(result.links), 1)
    self.assertEqual(result.links[0].url, "/a")

  async def test_async_crawl_many(self):
    pages = {
      "https://example.com/1": "<html><head><title>One</title></head></html>",
      "https://example.com/2": "<html><head><title>Two</title></head></html>",
    }
    engine = AsyncWebWeaveX(fetcher=MappingAsyncFetcher(pages))
    results = await engine.crawl_many(list(pages.keys()))
    titles = [result.metadata.title for result in results]
    self.assertEqual(titles, ["One", "Two"])

  async def test_concurrency_limit(self):
    config = CrawlConfig(max_concurrency=2)
    fetcher = ConcurrencyFetcher()
    crawler = AsyncCrawler(fetcher, config)
    urls = [f"https://example.com/{i}" for i in range(5)]
    await crawler.crawl_many(urls)
    self.assertLessEqual(fetcher.max_active, config.max_concurrency)


if __name__ == "__main__":
  unittest.main()
