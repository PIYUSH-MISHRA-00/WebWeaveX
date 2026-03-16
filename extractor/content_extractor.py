from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag


@dataclass
class ExtractedContent:
  title: str | None
  content_html: str


def _strip_boilerplate(soup: BeautifulSoup) -> None:
  for tag in soup.find_all(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
    tag.decompose()

  for tag in soup.find_all(True):
    if not isinstance(tag, Tag) or not hasattr(tag, "get") or tag.attrs is None:
      continue
    class_id = " ".join(filter(None, [tag.get("class")[0] if tag.get("class") else "", tag.get("id") or ""]))
    lowered = class_id.lower()
    if any(key in lowered for key in ["nav", "menu", "sidebar", "footer", "header", "breadcrumb"]):
      tag.decompose()


def _select_content_root(soup: BeautifulSoup) -> Tag:
  main = soup.find("main")
  if main:
    return main
  body = soup.find("body")
  if body:
    return body
  return soup


def _collect_blocks(root: Tag) -> list[Tag]:
  candidates = root.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "pre", "code"])
  selected: list[Tag] = []
  selected_set: set[int] = set()

  for tag in candidates:
    parent = tag.parent
    while parent is not None:
      if id(parent) in selected_set:
        break
      parent = parent.parent
    else:
      selected.append(tag)
      selected_set.add(id(tag))

  return selected


def extract_content(html: str) -> ExtractedContent:
  soup = BeautifulSoup(html or "", "html.parser")
  title = None
  if soup.title and soup.title.string:
    title = soup.title.string.strip() or None

  _strip_boilerplate(soup)
  root = _select_content_root(soup)

  blocks = _collect_blocks(root)
  wrapper = BeautifulSoup("<div></div>", "html.parser")
  container = wrapper.div
  for block in blocks:
    container.append(block)

  return ExtractedContent(title=title, content_html=container.decode_contents() if container else "")
