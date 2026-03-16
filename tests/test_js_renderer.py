import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from webweavex.config import CrawlConfig
from webweavex.js_renderer import JSRenderer


class FakePage:
  def __init__(self, state: dict) -> None:
    self._state = state

  async def goto(self, url: str, wait_until: str | None = None):
    self._state["goto"] = url
    self._state["wait_until"] = wait_until

  async def wait_for_selector(self, selector: str, timeout: int | None = None):
    self._state["selector"] = selector
    self._state["selector_timeout"] = timeout

  async def wait_for_timeout(self, timeout: int):
    self._state["timeout"] = timeout

  async def content(self) -> str:
    return "<html><body>Rendered</body></html>"


class FakeBrowser:
  def __init__(self, state: dict) -> None:
    self._state = state

  async def new_page(self) -> FakePage:
    return FakePage(self._state)

  async def close(self) -> None:
    self._state["browser_closed"] = True


class FakeChromium:
  def __init__(self, state: dict) -> None:
    self._state = state

  async def launch(self, headless: bool = True) -> FakeBrowser:
    self._state["headless"] = headless
    return FakeBrowser(self._state)


class FakePlaywright:
  def __init__(self, state: dict) -> None:
    self.chromium = FakeChromium(state)

  async def __aenter__(self):
    return self

  async def __aexit__(self, exc_type, exc, tb):
    return None


class JSRendererTests(unittest.IsolatedAsyncioTestCase):
  async def test_js_renderer_returns_html(self):
    state: dict = {}
    config = CrawlConfig(js_wait_time=0.1, js_wait_for_selector="#app", js_headless=True)
    renderer = JSRenderer(config, playwright_factory=lambda: FakePlaywright(state))

    html = await renderer.render("https://example.com")

    self.assertIn("Rendered", html)
    self.assertEqual(state.get("selector"), "#app")
    self.assertTrue(state.get("headless"))


if __name__ == "__main__":
  unittest.main()
