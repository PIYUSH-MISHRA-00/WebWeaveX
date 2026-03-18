# WebWeaveX Python SDK

## Installation
```bash
pip install webweavex
```

## Quick Start
```python
from sdk.python.webweavex_client import WebWeaveXClient

with WebWeaveXClient("http://127.0.0.1:8001") as client:
    result = client.crawl("https://example.com")
    print(result["status"])
```

## Usage Examples
```python
client = WebWeaveXClient("http://127.0.0.1:8001")
page = client.crawl("https://example.com")
dataset = client.rag_dataset("https://example.com")
graph = client.knowledge_graph("https://example.com")
client.close()
```

## API Reference
`WebWeaveXClient(base_url: str, timeout: float = 10.0)`

`crawl(url: str) -> dict`

`crawl_site(url: str) -> list[dict]`

`rag_dataset(url: str) -> list[dict]`

`knowledge_graph(url: str) -> dict`

## Example Output
```json
{
  "url": "https://example.com",
  "status": 200,
  "metadata": {
    "title": "Example Domain"
  }
}
```

## Error Handling
HTTP failures raise exceptions from `httpx` (`HTTPStatusError` and transport errors). Wrap SDK calls with `try/except` for retry or fallback logic.

## Security Notes
Use HTTPS for production API endpoints, validate untrusted URLs before crawling, and enforce egress/network policies in deployment environments.
