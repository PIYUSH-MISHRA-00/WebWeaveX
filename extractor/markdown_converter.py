from __future__ import annotations

from bs4 import BeautifulSoup

try:
  from markdownify import markdownify as to_markdown
except ImportError:  # pragma: no cover - fallback when markdownify is unavailable
  to_markdown = None


def html_to_markdown(html: str) -> str:
  if to_markdown:
    return to_markdown(html or "", heading_style="atx", code_style="fenced")

  soup = BeautifulSoup(html or "", "html.parser")
  lines: list[str] = []
  for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre"]):
    if tag.name and tag.name.startswith("h"):
      level = int(tag.name[1])
      lines.append(f"{'#' * level} {tag.get_text(strip=True)}")
    elif tag.name == "p":
      lines.append(tag.get_text(strip=True))
    elif tag.name == "li":
      lines.append(f"- {tag.get_text(strip=True)}")
    elif tag.name == "pre":
      code = tag.get_text()
      lines.append("```")
      lines.append(code.strip())
      lines.append("```")
  return "\n\n".join(line for line in lines if line)
