from __future__ import annotations

from webweavex.logging import get_logger
from webweavex.models import PageResult

from semantic.entity_extractor import extract_entities
from semantic.relationship_extractor import extract_relationships

from .graph_builder import build_graph as build_graph_structure

logger = get_logger(__name__)


def build_graph(pages: list[PageResult]) -> dict[str, list[dict[str, str]]]:
  entities: list[dict[str, str]] = []
  relationships: list[dict[str, str]] = []

  for page in pages:
    if not page.text:
      continue
    entities.extend(extract_entities(page.text))
    relationships.extend(extract_relationships(page.text))

  graph = build_graph_structure(entities, relationships)
  logger.info("Knowledge graph built")
  return graph
