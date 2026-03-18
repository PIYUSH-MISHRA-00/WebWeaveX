# WebWeaveX

**The web ingestion toolkit for AI teams: crawl once, ship structured data everywhere.**

[![CI](https://github.com/PIYUSH-MISHRA-00/WebWeaveX/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PIYUSH-MISHRA-00/WebWeaveX/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/PIYUSH-MISHRA-00/WebWeaveX/releases)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

## 10-Second Demo

```bash
uvicorn core.webweavex.api_server:app --port 8001
python cli/webweavex.py crawl https://example.com
```

Expected: JSON with `status: 200`, page metadata, and extracted links.

## Ultra Simple Example

```python
from sdk.python.webweavex_client import WebWeaveXClient

with WebWeaveXClient("http://127.0.0.1:8001") as client:
  print(client.crawl("https://example.com")["status"])
```

## Why This Exists

Most teams still stitch together crawler scripts, custom cleaners, and separate graph/RAG jobs. That creates fragile pipelines and duplicated failure handling. WebWeaveX exists to make web ingestion predictable, language-agnostic, and production-ready from day one.

- One API for crawl, RAG datasets, and knowledge graphs.
- Multi-language SDKs for Python, Node.js, Dart, Java, and Kotlin.
- Production defaults: timeout controls, retries, SSL verification, typed responses (Java/Kotlin).
- CLI + API + docs website in one repository.

## Comparison

| Capability | DIY Scraper Scripts | HTML Parser Libraries | WebWeaveX |
| --- | --- | --- | --- |
| Single-page crawl | Usually | Yes | Yes |
| Site crawl orchestration | Manual | No | Yes |
| RAG dataset output | Manual | No | Yes |
| Knowledge graph output | Manual | No | Yes |
| Multi-language SDKs | Rare | No | Yes |
| Built-in retry/timeout handling | Usually partial | No | Yes |

## Features

- Async crawler engine with SSL-aware fetch pipeline.
- REST API for crawl, site crawl, RAG dataset generation, and knowledge graph extraction.
- SDKs with timeout + retry/backoff controls in all supported languages.
- Portable CLI for local workflows and automation.
- Docusaurus-powered docs site for onboarding and reference.

## Quick Start

1. Install dependencies and local package:
```bash
python -m pip install -e .
```

2. Start API:
```bash
uvicorn core.webweavex.api_server:app --port 8001
```

3. Run a crawl from CLI:
```bash
python cli/webweavex.py crawl https://example.com
```

4. Hit API directly:
```bash
curl -X POST http://127.0.0.1:8001/crawl -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"
```

## Multi-Language SDKs

| Language | Path | Install | Example |
| --- | --- | --- | --- |
| Python | `sdk/python` | `pip install webweavex` | `python examples/python_client.py` |
| Node.js | `sdk/node` | `npm install webweavex` | `node examples/node_client.js` |
| Dart | `sdk/dart` | `dart pub add webweavex` | `dart run examples/dart_client.dart` |
| Java | `sdk/java` | Maven `io.webweavex:webweavex-java:0.1.0` | `mvn -f sdk/java/pom.xml exec:java` |
| Kotlin | `sdk/kotlin` | Maven `io.webweavex:webweavex-kotlin:0.1.0` | `mvn -f sdk/kotlin/pom.xml exec:java` |

SDK one-liners:

- Python: `WebWeaveXClient("http://127.0.0.1:8001").crawl("https://example.com")`
- Node.js: `await new WebWeaveXClient("http://127.0.0.1:8001").crawl("https://example.com")`
- Dart: `await WebWeaveXClient("http://127.0.0.1:8001").crawl("https://example.com")`
- Java: `new WebWeaveXClient("http://127.0.0.1:8001").crawl("https://example.com")`
- Kotlin: `WebWeaveXClient("http://127.0.0.1:8001").crawl("https://example.com")`

## Architecture

```text
           +------------------------------+
           |          CLI (Python)        |
           +---------------+--------------+
                           |
                           v
+--------------------------+--------------------------+
|                 Core Engine (Async)                 |
| fetch -> parse -> extract -> normalize -> model     |
+---------------+--------------------+----------------+
                |                    |
                v                    v
      +---------+---------+  +-------+----------------+
      |   REST API        |  | RAG + Knowledge Graph  |
      | /crawl            |  | /rag_dataset           |
      | /crawl_site       |  | /knowledge_graph       |
      +---------+---------+  +------------------------+
                |
                v
      +---------+-------------------------------------+
      | SDKs: Python | Node | Dart | Java | Kotlin   |
      +-----------------------------------------------+
```

## Use Cases

- Crawl public docs and turn them into clean RAG training/evaluation corpora.
- Build knowledge graphs from websites for search, reasoning, and discovery.
- Run SEO and content audits with normalized metadata + link extraction.
- Integrate web ingestion into backend pipelines with language-native SDKs.

## Benchmarks

Measured on local runs against deterministic sample targets:

| Scenario | Input | Result |
| --- | --- | --- |
| Single-page crawl | `https://example.com` | `200` status with metadata + links |
| API crawl endpoint | `/crawl` | JSON response under retry-safe transport |
| Multi-SDK smoke run | Python, Node, Dart, Java, Kotlin | All clients returned valid JSON payloads |
| Website docs build | Docusaurus production build | Static output generated successfully |

Repro scripts live in `benchmarks/`.

## Roadmap

- Streaming crawl endpoint for large-site pipelines.
- Auth + rate-limit policies for hosted deployments.
- First-class observability pack (metrics + tracing dashboards).
- Expanded examples for enterprise SSO docs and multi-tenant usage.
- Package publishing automation for PyPI, npm, pub.dev, and Maven Central.

## Release Notes

- `v0.1.0`: `docs/releases/v0.1.0.md`

## Repository Structure

- `core/` engine, models, API server
- `cli/` command-line entrypoint
- `sdk/` all language clients
- `website/` Docusaurus docs site
- `examples/` runnable SDK demos
- `docs/` additional technical docs
- `reports/` verification artifacts including `reports/FINAL_PROOF.md`

## License

Apache-2.0. See `LICENSE`.
