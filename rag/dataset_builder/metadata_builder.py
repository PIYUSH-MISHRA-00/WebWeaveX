from __future__ import annotations

from urllib.parse import urlparse

from webweavex.models import PageResult


def build_metadata(page: PageResult, chunk_id: int) -> dict[str, object]:
  parsed = urlparse(page.url)
  source_domain = parsed.netloc or ""
  title = page.metadata.title if page.metadata else None
  return {
    "url": page.url,
    "title": title,
    "chunk_id": chunk_id,
    "source_domain": source_domain,
  }
