# WebWeaveX Python SDK

## Installation
```bash
pip install webweavex
```

## Quick Start
```python
from sdk.python.webweavex_client import WebWeaveXClient

with WebWeaveXClient("http://127.0.0.1:8001", timeout=10.0, max_retries=2) as client:
  page = client.crawl("https://example.com")
  print(page["status"])
```

## Usage Examples
```python
from sdk.python.webweavex_client import WebWeaveXClient

client = WebWeaveXClient(
  "http://127.0.0.1:8001",
  timeout=8.0,
  max_retries=3,
  backoff_seconds=0.4,
)

page = client.crawl("https://example.com")
dataset = client.rag_dataset("https://example.com")
graph = client.knowledge_graph("https://example.com")

client.close()
```

## API Reference
`WebWeaveXClient(base_url: str, timeout: float = 10.0, max_retries: int = 2, backoff_seconds: float = 0.3, retry_statuses: set[int] | None = None)`

`crawl(url: str) -> dict[str, Any]`

`crawl_site(url: str) -> list[dict[str, Any]]`

`rag_dataset(url: str) -> list[dict[str, Any]]`

`knowledge_graph(url: str) -> dict[str, list[dict[str, str]]]`

Errors:

`WebWeaveXError`

`WebWeaveXTimeoutError`

`WebWeaveXNetworkError`

`WebWeaveXHTTPError`

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
```python
from sdk.python.webweavex_client import WebWeaveXClient, WebWeaveXTimeoutError, WebWeaveXHTTPError

client = WebWeaveXClient("http://127.0.0.1:8001", max_retries=2)
try:
  client.crawl("https://example.com")
except WebWeaveXTimeoutError:
  print("Retry budget exhausted due to timeout")
except WebWeaveXHTTPError as exc:
  print(exc.status_code, exc.response_body)
```

## Security Notes
- Use HTTPS for production API endpoints.
- Validate and sanitize user-supplied URLs before crawl requests.
- Apply network egress policies so crawler workers can only reach approved domains.
