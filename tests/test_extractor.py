import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from extractor.content_extractor import extract_content
from extractor.extraction_pipeline import process
from extractor.markdown_converter import html_to_markdown
from webweavex.models import PageResult


class ExtractorTests(unittest.TestCase):
  def test_html_to_markdown(self):
    html = """
    <html>
      <head><title>Doc</title></head>
      <body>
        <main>
          <h1>Intro</h1>
          <p>Hello world</p>
          <ul><li>Item A</li></ul>
          <pre><code>print("hi")</code></pre>
        </main>
      </body>
    </html>
    """
    extracted = extract_content(html)
    markdown = html_to_markdown(extracted.content_html)

    self.assertIn("# Intro", markdown)
    self.assertIn("Hello world", markdown)
    self.assertIn("Item A", markdown)
    self.assertIn("```", markdown)
    self.assertIn("print(\"hi\")", markdown)

class ExtractorPipelineTests(unittest.IsolatedAsyncioTestCase):
  async def test_pipeline_preserves_headings_and_code(self):
    html = """
    <html>
      <head><title>Doc</title></head>
      <body>
        <nav>Home</nav>
        <main>
          <h2>Section</h2>
          <p>Paragraph</p>
          <pre><code>const a = 1;</code></pre>
        </main>
      </body>
    </html>
    """
    page = PageResult(url="https://example.com", status=200, html=html)
    processed = await process(page)

    self.assertIsNotNone(processed.markdown)
    self.assertIn("## Section", processed.markdown)
    self.assertIn("```", processed.markdown)
    self.assertIn("const a = 1", processed.markdown)
    self.assertIsNotNone(processed.text)
    self.assertNotIn("Home", processed.text)


if __name__ == "__main__":
  unittest.main()
