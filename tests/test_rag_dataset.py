import json
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from rag.chunking.text_chunker import chunk_text
from rag.dataset_builder.exporter import export_csv, export_jsonl, export_markdown
from rag.dataset_builder.metadata_builder import build_metadata
from rag.dataset_builder.rag_dataset import build_dataset_entries
from webweavex.models import Metadata, PageResult


class RagDatasetTests(unittest.TestCase):
  def test_chunking(self):
    text = "A" * 1200
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
    self.assertEqual(len(chunks), 3)
    self.assertEqual(chunks[0]["chunk_id"], 1)
    self.assertEqual(len(chunks[0]["text"]), 500)
    self.assertEqual(len(chunks[1]["text"]), 500)
    self.assertGreater(len(chunks[2]["text"]), 0)

  def test_metadata_generation(self):
    page = PageResult(
      url="https://example.com/path",
      status=200,
      html=None,
      links=[],
      metadata=Metadata(title="Title"),
    )
    meta = build_metadata(page, 1)
    self.assertEqual(meta["url"], "https://example.com/path")
    self.assertEqual(meta["title"], "Title")
    self.assertEqual(meta["chunk_id"], 1)
    self.assertEqual(meta["source_domain"], "example.com")

  def test_dataset_export(self):
    page = PageResult(
      url="https://example.com/path",
      status=200,
      html=None,
      links=[],
      metadata=Metadata(title="Title"),
      text="Hello world",
    )
    entries = build_dataset_entries([page], chunk_size=5, chunk_overlap=0)
    self.assertGreater(len(entries), 1)

    with tempfile.TemporaryDirectory() as tmpdir:
      jsonl_path = Path(tmpdir) / "data.jsonl"
      csv_path = Path(tmpdir) / "data.csv"
      md_path = Path(tmpdir) / "data.md"

      export_jsonl(entries, jsonl_path)
      export_csv(entries, csv_path)
      export_markdown(entries, md_path)

      jsonl_content = jsonl_path.read_text(encoding="utf-8").strip().splitlines()
      self.assertGreaterEqual(len(jsonl_content), 1)
      parsed = json.loads(jsonl_content[0])
      self.assertIn("text", parsed)
      self.assertIn("url", parsed)

      csv_content = csv_path.read_text(encoding="utf-8")
      self.assertIn("url", csv_content)

      md_content = md_path.read_text(encoding="utf-8")
      self.assertIn("##", md_content)
      self.assertIn("Hello", md_content)


if __name__ == "__main__":
  unittest.main()
