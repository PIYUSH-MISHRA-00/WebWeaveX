import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from webweavex.crawler import parse_html
from webweavex.engine import WebWeaveX


class DummyFetcher:
  def __init__(self, html: str, status: int = 200) -> None:
    self._html = html
    self._status = status

  def fetch(self, url: str):
    return self._status, self._html


class EngineTests(unittest.TestCase):
  def test_basic_crawl(self):
    html = """
    <html>
      <head><title>Example</title></head>
      <body>
        <a href="https://example.com/a">Alpha</a>
      </body>
    </html>
    """
    engine = WebWeaveX(fetcher=DummyFetcher(html))
    result = engine.crawl("https://example.com")

    self.assertEqual(result.url, "https://example.com")
    self.assertEqual(result.status, 200)
    self.assertEqual(result.html.strip(), html.strip())
    self.assertEqual(result.metadata.title, "Example")
    self.assertEqual(len(result.links), 1)
    self.assertEqual(result.links[0].url, "https://example.com/a")
    self.assertEqual(result.links[0].text, "Alpha")

  def test_html_parsing_metadata(self):
    html = """
    <html>
      <head>
        <title>Meta Test</title>
        <meta name="description" content="A test page">
      </head>
      <body></body>
    </html>
    """
    links, metadata = parse_html(html)
    self.assertEqual(metadata.title, "Meta Test")
    self.assertEqual(metadata.meta.get("description"), "A test page")
    self.assertEqual(links, [])

  def test_link_extraction(self):
    html = """
    <html><body>
      <a href="/one">One</a>
      <a href="/two"></a>
    </body></html>
    """
    links, _ = parse_html(html)
    self.assertEqual(len(links), 2)
    self.assertEqual(links[0].url, "/one")
    self.assertEqual(links[0].text, "One")
    self.assertEqual(links[1].url, "/two")
    self.assertIsNone(links[1].text)


if __name__ == "__main__":
  unittest.main()
