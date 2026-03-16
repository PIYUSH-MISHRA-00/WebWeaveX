import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from knowledge_graph.graph_builder import build_graph
from knowledge_graph.graph_pipeline import build_graph as build_graph_from_pages
from semantic.entity_extractor import extract_entities
from semantic.relationship_extractor import extract_relationships
from webweavex.models import Metadata, PageResult


class KnowledgeGraphTests(unittest.TestCase):
  def test_entity_extraction(self):
    text = "Guido van Rossum created Python at OpenAI in San Francisco."
    entities = extract_entities(text)
    entity_names = {entity["entity"] for entity in entities}
    self.assertIn("Guido van Rossum", entity_names)
    self.assertIn("Python", entity_names)

  def test_relationship_extraction(self):
    text = "Guido van Rossum created Python. Alice founded Acme Corp. Bob works at OpenAI."
    relations = extract_relationships(text)
    self.assertTrue(any(rel["relation"] == "created" for rel in relations))
    self.assertTrue(any(rel["relation"] == "founded" for rel in relations))
    self.assertTrue(any(rel["relation"] == "works at" for rel in relations))

  def test_graph_builder(self):
    entities = [
      {"entity": "Guido van Rossum", "type": "PERSON"},
      {"entity": "Python", "type": "PRODUCT"},
    ]
    relations = [
      {"source": "Guido van Rossum", "relation": "created", "target": "Python"}
    ]
    graph = build_graph(entities, relations)
    node_ids = {node["id"] for node in graph["nodes"]}
    self.assertIn("Guido van Rossum", node_ids)
    self.assertIn("Python", node_ids)
    self.assertEqual(len(graph["edges"]), 1)

  def test_graph_pipeline(self):
    page = PageResult(
      url="https://example.com",
      status=200,
      html=None,
      links=[],
      metadata=Metadata(title="Test"),
      text="Guido van Rossum created Python.",
    )
    graph = build_graph_from_pages([page])
    self.assertGreaterEqual(len(graph["nodes"]), 2)
    self.assertGreaterEqual(len(graph["edges"]), 1)


if __name__ == "__main__":
  unittest.main()
