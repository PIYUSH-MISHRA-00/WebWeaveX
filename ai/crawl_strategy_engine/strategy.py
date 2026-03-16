from __future__ import annotations

from webweavex.logging import get_logger

logger = get_logger(__name__)


class CrawlStrategy:
  """Simple keyword-based scoring strategy for crawl prioritization."""

  def __init__(self, keywords: list[str] | None = None) -> None:
    self._keywords = [kw.lower() for kw in (keywords or [])]

  def score(self, url: str, anchor_text: str | None, page_text: str | None) -> float:
    url_lower = (url or "").lower()
    anchor_lower = (anchor_text or "").lower()
    page_lower = (page_text or "").lower()

    score = 0.0
    for keyword in self._keywords:
      if not keyword:
        continue
      if keyword in url_lower:
        score += 2.0
      if anchor_lower and keyword in anchor_lower:
        score += 1.0
      if page_lower and keyword in page_lower:
        score += 0.5

    logger.info("URL scored %s => %s", url, score)
    return score
