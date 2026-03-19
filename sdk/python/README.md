# WebWeaveX Python SDK

[![PyPI](https://img.shields.io/pypi/v/webweavex?label=PyPI)](https://pypi.org/project/webweavex/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](../../LICENSE)

Python SDK for [WebWeaveX](https://github.com/PIYUSH-MISHRA-00/WebWeaveX) — production-ready web crawling client with retry and backoff.

## Version

`0.1.0` · Python 3.9+ · PyPI

## Installation

```bash
pip install webweavex
```

## Quick Start

```python
from webweavex_client import WebWeaveXClient

# Context manager — auto-closes session
with WebWeaveXClient("http://localhost:8001") as client:
    # Crawl a single page
    page = client.crawl("https://example.com")
    print(page["status"])           # 200
    print(page["metadata"]["title"])

    # Generate RAG dataset
    records = client.rag_dataset("https://example.com")
    print(len(records), "chunks")

    # Extract knowledge graph
    kg = client.knowledge_graph("https://example.com")
    print(len(kg["nodes"]), "nodes")
```

## API Reference

| Method | Endpoint | Returns |
|---|---|---|
| `crawl(url)` | `/crawl` | `dict` |
| `crawl_site(url)` | `/crawl_site` | `list[dict]` |
| `rag_dataset(url)` | `/rag_dataset` | `list[dict]` |
| `knowledge_graph(url)` | `/knowledge_graph` | `dict` |

### Constructor Options

```python
WebWeaveXClient(
    base_url="http://localhost:8001",
    timeout=10.0,         # seconds
    max_retries=2,
    backoff_base=0.3,     # seconds
    retry_status_codes={408, 429, 500, 502, 503, 504},
    debug=False,
)
```

## Error Types

| Exception | Cause |
|---|---|
| `WebWeaveXError` | Base SDK exception |
| `WebWeaveXTimeoutError` | Request timed out |
| `WebWeaveXHTTPError` | Non-2xx HTTP response |
| `WebWeaveXNetworkError` | Network/connection failure |

## License

Apache-2.0
