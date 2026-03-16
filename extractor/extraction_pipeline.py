from __future__ import annotations

from webweavex.models import PageResult

from .content_extractor import extract_content
from .markdown_converter import html_to_markdown
from .text_cleaner import clean_text


def process(page: PageResult) -> PageResult:
  if not page.html:
    page.markdown = None
    page.text = None
    return page

  extracted = extract_content(page.html)
  markdown = html_to_markdown(extracted.content_html)
  cleaned_text = clean_text(markdown)

  page.markdown = markdown.strip() if markdown else None
  page.text = cleaned_text.strip() if cleaned_text else None
  return page
