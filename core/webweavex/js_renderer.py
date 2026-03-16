from __future__ import annotations

from .config import CrawlConfig
from .logging import get_logger

logger = get_logger(__name__)


class JSRenderer:
  """Render JavaScript-heavy pages using Playwright."""

  def __init__(self, config: CrawlConfig, playwright_factory=None) -> None:
    self._config = config
    self._playwright_factory = playwright_factory

  async def render(self, url: str) -> str:
    logger.info("Rendering JS for %s", url)
    if self._playwright_factory is None:
      from playwright.async_api import async_playwright

      playwright_factory = async_playwright
    else:
      playwright_factory = self._playwright_factory

    async with playwright_factory() as playwright:
      browser = await playwright.chromium.launch(headless=self._config.js_headless)
      page = await browser.new_page()
      await page.goto(url, wait_until="domcontentloaded")

      timeout_ms = int(self._config.js_wait_time * 1000)
      if self._config.js_wait_for_selector:
        await page.wait_for_selector(self._config.js_wait_for_selector, timeout=timeout_ms)
      else:
        await page.wait_for_timeout(timeout_ms)

      html = await page.content()
      await browser.close()
      return html
