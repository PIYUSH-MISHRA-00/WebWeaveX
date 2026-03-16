import sys
from pathlib import Path
import unittest

import httpx

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from webweavex.async_crawler import AsyncCrawler
from webweavex.config import CrawlConfig
from webweavex.robots import RobotsHandler


class RobotsTests(unittest.IsolatedAsyncioTestCase):
  async def test_robots_blocks_url(self):
    robots_txt = """
    User-agent: *
    Disallow: /blocked
    """

    async def handler(request):
      return httpx.Response(200, text=robots_txt)

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(transport=transport)
    robots = RobotsHandler(CrawlConfig(), client=client)

    allowed = await robots.allowed("https://example.com/blocked")

    self.assertFalse(allowed)
    await client.aclose()

  async def test_crawler_obeys_robots(self):
    class DenyRobots:
      async def allowed(self, url: str) -> bool:
        return False

    class ExplodingFetcher:
      async def fetch(self, url: str):
        raise AssertionError("Fetcher should not be called for blocked URLs")

    crawler = AsyncCrawler(ExplodingFetcher(), CrawlConfig(), robots=DenyRobots())
    result = await crawler.crawl("https://example.com/blocked")

    self.assertEqual(result.status, 403)
    self.assertIsNone(result.html)


if __name__ == "__main__":
  unittest.main()
