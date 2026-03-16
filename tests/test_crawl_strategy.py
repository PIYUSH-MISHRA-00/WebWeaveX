import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from ai.crawl_strategy_engine.strategy import CrawlStrategy
from frontier.url_frontier import URLFrontier


class CrawlStrategyTests(unittest.TestCase):
  def test_scoring(self):
    strategy = CrawlStrategy(["docs", "api", "guide"])
    score = strategy.score(
      "https://example.com/docs/api",
      "guide",
      "This page is an API guide.",
    )
    self.assertGreaterEqual(score, 3.5)

  def test_priority_frontier(self):
    frontier = URLFrontier(max_depth=2)
    frontier.add("https://example.com/low", depth=0, priority=1.0)
    frontier.add("https://example.com/high", depth=0, priority=3.0)
    frontier.add("https://example.com/mid", depth=0, priority=2.0)

    first = frontier.next()
    second = frontier.next()
    third = frontier.next()

    self.assertEqual(first[0], "https://example.com/high")
    self.assertEqual(second[0], "https://example.com/mid")
    self.assertEqual(third[0], "https://example.com/low")


if __name__ == "__main__":
  unittest.main()
