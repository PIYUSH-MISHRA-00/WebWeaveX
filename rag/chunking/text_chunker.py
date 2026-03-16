from __future__ import annotations

from webweavex.logging import get_logger

logger = get_logger(__name__)


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict[str, object]]:
  """Split text into overlapping chunks."""
  if not text:
    return []

  if chunk_size <= 0:
    raise ValueError("chunk_size must be positive")

  overlap = max(0, min(chunk_overlap, chunk_size - 1))
  chunks: list[dict[str, object]] = []
  index = 0
  chunk_id = 1
  text_length = len(text)

  while index < text_length:
    end = index + chunk_size
    chunk = text[index:end].strip()
    if chunk:
      chunks.append({"text": chunk, "chunk_id": chunk_id})
      chunk_id += 1
    if end >= text_length:
      break
    index = end - overlap

  logger.info("Chunks created %s", len(chunks))
  return chunks
