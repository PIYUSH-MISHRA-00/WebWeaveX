# WebWeaveX

WebWeaveX is a multi-language web crawling platform with a Python core engine, REST API, and SDKs for Python, Node.js, Dart, Java, and Kotlin.

## Features
- Async-first crawler with SSL verification and retry handling.
- REST API for crawl, RAG dataset generation, and knowledge graph generation.
- CLI workflows for one-shot crawl, site crawl, graph export, and RAG export.
- Multi-language SDKs for integrating WebWeaveX into existing stacks.
- Docusaurus website/docs for developer onboarding.

## Architecture
`cli/` provides command-line entrypoints.

`core/webweavex/` contains crawler, fetcher, parser, API server, and domain models.

`rag/` and `knowledge_graph/` convert crawl results into downstream AI-ready artifacts.

`sdk/` hosts language SDK implementations.

`website/` renders documentation and product-facing docs.

## CLI Demo
```bash
python cli/webweavex.py crawl https://example.com
```

Expected output includes:
- `status: 200`
- page metadata title (`Example Domain`)
- extracted links

## API Demo
```bash
uvicorn core.webweavex.api_server:app --port 8001
```

```bash
curl -X POST http://127.0.0.1:8001/crawl -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"
curl -X POST http://127.0.0.1:8001/rag_dataset -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"
curl -X POST http://127.0.0.1:8001/knowledge_graph -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"
```

## SDK Examples
### Python
```python
from sdk.python.webweavex_client import WebWeaveXClient
with WebWeaveXClient("http://127.0.0.1:8001") as client:
    print(client.crawl("https://example.com")["status"])
```

### Node.js
```javascript
const { WebWeaveXClient } = require("./sdk/node/index");
const client = new WebWeaveXClient("http://127.0.0.1:8001");
client.crawl("https://example.com").then(console.log);
```

### Dart
```dart
import 'sdk/dart/lib/webweavex.dart';

final client = WebWeaveXClient('http://127.0.0.1:8001');
final result = await client.crawl('https://example.com');
print(result['status']);
```

### Java
```java
WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
System.out.println(client.crawl("https://example.com").get("status"));
```

### Kotlin
```kotlin
val client = WebWeaveXClient("http://127.0.0.1:8001")
println(client.crawl("https://example.com"))
```

## Use Cases
- SEO and web quality monitoring.
- RAG dataset construction from public documentation sites.
- Knowledge graph extraction from link structure and metadata.
- Developer tooling for scheduled crawl pipelines.

## Benchmarks
Benchmark scripts are in `benchmarks/`:
- `python benchmarks/crawl_speed.py`
- `python benchmarks/distributed_scaling.py`
- `python benchmarks/js_rendering.py`

Baseline validation in this repo verifies successful HTTPS crawl responses (`200`) against `https://example.com` across CLI, API, and all SDK examples.
