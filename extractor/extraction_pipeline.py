from __future__ import annotations

from webweavex.logging import get_logger
from webweavex.models import PageResult
from webweavex.plugin_loader import get_plugins

from .content_extractor import extract_content
from .markdown_converter import html_to_markdown
from .text_cleaner import clean_text

logger = get_logger(__name__)


async def process(page: PageResult) -> PageResult:
  if not page.html:
    page.markdown = None
    page.text = None
    return page

  extracted = extract_content(page.html)
  markdown = html_to_markdown(extracted.content_html)
  cleaned_text = clean_text(markdown)

  page.markdown = markdown.strip() if markdown else None
  page.text = cleaned_text.strip() if cleaned_text else None

  await _run_plugins(page)
  return page


async def _run_plugins(page: PageResult) -> None:
  plugins = get_plugins()
  if not plugins:
    return

  for plugin in plugins:
    try:
      if plugin.supports(page.url):
        plugin_name = getattr(plugin, "name", plugin.__class__.__name__)
        logger.info("Plugin executed %s for %s", plugin_name, page.url)
        await plugin.process(page)
    except Exception:
      plugin_name = getattr(plugin, "name", plugin.__class__.__name__)
      logger.exception("Plugin failed %s for %s", plugin_name, page.url)
