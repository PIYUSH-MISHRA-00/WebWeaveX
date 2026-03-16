from __future__ import annotations

from webweavex.logging import get_logger

logger = get_logger(__name__)


def build_graph(
  entities: list[dict[str, str]],
  relationships: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
  nodes: dict[str, str] = {}
  for entity in entities:
    name = entity.get("entity")
    label = entity.get("type") or "Entity"
    if name:
      nodes[name] = label

  for relation in relationships:
    source = relation.get("source")
    target = relation.get("target")
    if source and source not in nodes:
      nodes[source] = "Entity"
    if target and target not in nodes:
      nodes[target] = "Entity"

  node_list = [{"id": node_id, "label": label} for node_id, label in nodes.items()]
  edge_list = [
    {
      "source": rel.get("source", ""),
      "target": rel.get("target", ""),
      "relation": rel.get("relation", ""),
    }
    for rel in relationships
  ]

  logger.info("Graph built with %s nodes and %s edges", len(node_list), len(edge_list))
  return {"nodes": node_list, "edges": edge_list}
