from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from webweavex.models import PageResult
from webweavex.plugin_interface import WebWeaveXPlugin


class YouTubePlugin(WebWeaveXPlugin):
  name = "youtube"

  def supports(self, url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    return "youtube.com" in host or "youtu.be" in host

  async def process(self, page: PageResult) -> None:
    if not page.html:
      return

    soup = BeautifulSoup(page.html, "html.parser")
    title = (
      _meta_content(soup, "og:title")
      or _meta_content(soup, "title")
      or (soup.title.string.strip() if soup.title and soup.title.string else None)
    )
    description = _meta_content(soup, "og:description") or _meta_content(
      soup, "description", attr="name"
    )
    channel = (
      _meta_content(soup, "channelId", attr="itemprop")
      or _meta_content(soup, "author", attr="itemprop")
      or _meta_content(soup, "name", attr="itemprop")
    )
    video_id = _extract_video_id(page.url)

    if title and not page.metadata.title:
      page.metadata.title = title

    page.metadata.meta["youtube"] = {
      "title": title,
      "description": description,
      "channel": channel,
      "video_id": video_id,
    }


def _meta_content(soup: BeautifulSoup, value: str, attr: str = "property") -> str | None:
  tag = soup.find("meta", attrs={attr: value})
  if tag and tag.get("content"):
    return tag["content"].strip()
  return None


def _extract_video_id(url: str) -> str | None:
  parsed = urlparse(url)
  if parsed.netloc.endswith("youtu.be"):
    return parsed.path.lstrip("/") or None
  query = parse_qs(parsed.query)
  video_ids = query.get("v", [])
  if video_ids:
    return video_ids[0]
  return None
