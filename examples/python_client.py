import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from sdk.python.webweavex_client import WebWeaveXClient


def main() -> None:
  with WebWeaveXClient("http://127.0.0.1:8001") as client:
    result = client.crawl("https://example.com")

  print("Python SDK test passed")
  print(f"Status: {result['status']}")
  print(f"URL: {result['url']}")
  print(f"Title: {result['metadata']['title']}")


if __name__ == "__main__":
  main()
