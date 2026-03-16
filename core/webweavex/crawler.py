from __future__ import annotations

from bs4 import BeautifulSoup

from .config import CrawlConfig
from .exceptions import ParseError
from .fetcher import HttpFetcher
from .models import Link, Metadata, PageResult


def parse_html(html: str | None) -> tuple[list[Link], Metadata]:
  if not html:
    return [], Metadata()

  try:
    soup = BeautifulSoup(html, "html.parser")
  except Exception as exc:
    raise ParseError("Failed to parse HTML") from exc

  title = None
  if soup.title and soup.title.string:
    title = soup.title.string.strip() or None

  meta: dict[str, str] = {}
  for tag in soup.find_all("meta"):
    name = tag.get("name") or tag.get("property") or tag.get("http-equiv")
    content = tag.get("content")
    if name and content:
      meta[name] = content

  links: list[Link] = []
  for tag in soup.find_all("a"):
    href = tag.get("href")
    if not href:
      continue
    text = tag.get_text(strip=True) or None
    links.append(Link(url=href, text=text))

  return links, Metadata(title=title, meta=meta)


class Crawler:
  """Core crawler that fetches and parses a single URL."""

  def __init__(self, fetcher: HttpFetcher, config: CrawlConfig) -> None:
    self._fetcher = fetcher
    self._config = config

  def crawl(self, url: str) -> PageResult:
    status, html = self._fetcher.fetch(url)
    links, metadata = parse_html(html)
    return PageResult(url=url, status=status, html=html, links=links, metadata=metadata)
