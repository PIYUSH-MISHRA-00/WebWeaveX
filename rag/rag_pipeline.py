from __future__ import annotations

from webweavex.logging import get_logger
from webweavex.models import PageResult

from rag.dataset_builder.rag_dataset import build_dataset_entries

logger = get_logger(__name__)


def build_dataset(
  pages: list[PageResult],
  chunk_size: int = 500,
  chunk_overlap: int = 50,
) -> list[dict[str, object]]:
  logger.info("Dataset generation started")
  return build_dataset_entries(pages, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
