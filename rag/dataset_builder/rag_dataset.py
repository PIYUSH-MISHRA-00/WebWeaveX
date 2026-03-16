from __future__ import annotations

from webweavex.logging import get_logger
from webweavex.models import PageResult

from rag.chunking.text_chunker import chunk_text
from rag.dataset_builder.metadata_builder import build_metadata

logger = get_logger(__name__)


def build_dataset_entries(
  pages: list[PageResult],
  chunk_size: int = 500,
  chunk_overlap: int = 50,
) -> list[dict[str, object]]:
  entries: list[dict[str, object]] = []
  for page in pages:
    if not page.text:
      continue
    chunks = chunk_text(page.text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    for chunk in chunks:
      metadata = build_metadata(page, int(chunk["chunk_id"]))
      entry = {
        "text": chunk["text"],
        **metadata,
      }
      entries.append(entry)

  logger.info("Dataset size %s", len(entries))
  return entries
