# WebWeaveX

**The web ingestion toolkit for AI teams — crawl once, ship structured data everywhere.**

[![Maven Central](https://img.shields.io/maven-central/v/io.github.piyush-mishra-00/webweavex?label=Maven%20Central)](https://central.sonatype.com/artifact/io.github.piyush-mishra-00/webweavex)
[![PyPI](https://img.shields.io/pypi/v/webweavex?label=PyPI)](https://pypi.org/project/webweavex/)
[![npm](https://img.shields.io/npm/v/webweavex?label=npm)](https://www.npmjs.com/package/webweavex)
[![pub.dev](https://img.shields.io/pub/v/webweavex?label=pub.dev)](https://pub.dev/packages/webweavex)
[![CI](https://github.com/PIYUSH-MISHRA-00/WebWeaveX/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PIYUSH-MISHRA-00/WebWeaveX/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

---

## What is WebWeaveX?

WebWeaveX is a production-ready, multi-language SDK platform for AI-native web crawling. It provides a single REST API with typed SDKs for **Python**, **Node.js**, **Dart**, **Java**, and **Kotlin**, each with built-in retry/backoff, timeout controls, and structured error types.

| Capability | DIY Scripts | HTML Parsers | WebWeaveX |
|---|---|---|---|
| Single-page crawl | Usually | Yes | ✅ |
| Site crawl orchestration | Manual | No | ✅ |
| RAG dataset output | Manual | No | ✅ |
| Knowledge graph extraction | Manual | No | ✅ |
| Multi-language typed SDKs | Rare | No | ✅ |
| Built-in retry + backoff | Partial | No | ✅ |

---

## Installation

### Python
```bash
pip install webweavex
```

### Node.js
```bash
npm install webweavex
```

### Dart
```bash
dart pub add webweavex
```

### Java (Maven)
```xml
<dependency>
  <groupId>io.github.piyush-mishra-00</groupId>
  <artifactId>webweavex</artifactId>
  <version>0.1.0</version>
</dependency>
```

### Kotlin (Gradle Kotlin DSL)
```kotlin
implementation("io.github.piyush-mishra-00:webweavex-kotlin:0.1.0")
```

---

## Quick Start

### Python
```python
from webweavex_client import WebWeaveXClient

with WebWeaveXClient("http://localhost:8001") as client:
    result = client.crawl("https://example.com")
    print(result["status"])   # 200
    records = client.rag_dataset("https://example.com")
    kg = client.knowledge_graph("https://example.com")
```

### Node.js
```js
const { WebWeaveXClient } = require("webweavex");

const client = new WebWeaveXClient("http://localhost:8001");
const result = await client.crawl("https://example.com");
console.log(result.status);   // 200
```

### Dart
```dart
import 'package:webweavex/webweavex.dart';

final client = WebWeaveXClient('http://localhost:8001');
final result = await client.crawl('https://example.com');
client.close();
```

### Java
```java
var client = new WebWeaveXClient("http://localhost:8001");
PageResult page = client.crawl("https://example.com");
System.out.println(page.getStatus());   // 200
```

### Kotlin
```kotlin
import io.github.piyushmishra.webweavex.WebWeaveX

val client = WebWeaveX.create {
    baseUrl = "http://localhost:8001"
    retries = 3
}
val result = client.crawl("https://example.com")
println(result["status"])
client.close()
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/crawl` | POST | Crawl a single URL, returns page metadata, HTML, links, markdown |
| `/crawl_site` | POST | Crawl an entire site, returns list of page results |
| `/rag_dataset` | POST | Generate a RAG-ready chunked dataset from a URL |
| `/knowledge_graph` | POST | Extract a knowledge graph (nodes + edges) from a URL |

---

## Repository Structure

```
WebWeaveX/
├── sdk/
│   ├── java/          Java SDK (Maven Central)
│   ├── kotlin/        Kotlin SDK (Maven Central)
│   ├── python/        Python SDK (PyPI)
│   ├── node/          Node.js SDK (npm)
│   └── dart/          Dart SDK (pub.dev)
├── website/           Static landing page (GitHub Pages)
├── core/              Core API server (FastAPI)
├── cli/               Command-line interface
├── examples/          Runnable SDK demos
├── docs/              Technical documentation
└── .github/workflows/ CI + release + pages pipelines
```

---

## Running the API Server

```bash
# Install dependencies
pip install -e .

# Start the server
uvicorn core.webweavex.api_server:app --port 8001

# Test via CLI
python cli/webweavex.py crawl https://example.com
```

---

## License

Apache-2.0. See [LICENSE](LICENSE).

---

> Built by [Piyush Mishra](https://github.com/PIYUSH-MISHRA-00) · [Website](https://piyush-mishra-00.github.io/WebWeaveX/)
