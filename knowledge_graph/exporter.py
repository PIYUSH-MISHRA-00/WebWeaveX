from __future__ import annotations

import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ElementTree


def export_json(graph: dict[str, list[dict[str, str]]], path: str | Path) -> None:
  output_path = Path(path)
  output_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")


def export_graphml(graph: dict[str, list[dict[str, str]]], path: str | Path) -> None:
  graphml = ElementTree.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
  ElementTree.SubElement(
    graphml,
    "key",
    id="label",
    **{"for": "node", "attr.name": "label", "attr.type": "string"},
  )
  ElementTree.SubElement(
    graphml,
    "key",
    id="relation",
    **{"for": "edge", "attr.name": "relation", "attr.type": "string"},
  )

  graph_el = ElementTree.SubElement(graphml, "graph", edgedefault="directed")

  for node in graph.get("nodes", []):
    node_el = ElementTree.SubElement(graph_el, "node", id=str(node.get("id", "")))
    data = ElementTree.SubElement(node_el, "data", key="label")
    data.text = node.get("label", "")

  for edge in graph.get("edges", []):
    edge_el = ElementTree.SubElement(
      graph_el,
      "edge",
      source=str(edge.get("source", "")),
      target=str(edge.get("target", "")),
    )
    data = ElementTree.SubElement(edge_el, "data", key="relation")
    data.text = edge.get("relation", "")

  tree = ElementTree.ElementTree(graphml)
  tree.write(Path(path), encoding="utf-8", xml_declaration=True)


def export_csv(
  graph: dict[str, list[dict[str, str]]],
  nodes_path: str | Path,
  edges_path: str | Path,
) -> None:
  nodes_file = Path(nodes_path)
  edges_file = Path(edges_path)

  with nodes_file.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["id", "label"])
    writer.writeheader()
    writer.writerows(graph.get("nodes", []))

  with edges_file.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["source", "target", "relation"])
    writer.writeheader()
    writer.writerows(graph.get("edges", []))
