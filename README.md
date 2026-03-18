# WebWeaveX

A high-performance web crawler and data extraction toolkit.

## Features
- Scalable distributed crawling
- Built-in RAG dataset generator
- Multi-language SDKs

## CLI Demo
```bash
python cli/webweavex.py crawl https://example.com
```

## Multi-Language SDK Examples

### Python
```python
import webweavex
```

### Node.js
```javascript
const client = new WebWeaveXClient("http://127.0.0.1:8001");
```

### Dart
```dart
final response = await http.post(Uri.parse('http://127.0.0.1:8001/crawl'));
```

### Java
```java
WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
```

### Kotlin
```kotlin
val client = WebWeaveXClient("http://127.0.0.1:8001")
```

## Architecture Overview
WebWeaveX offers a core REST API server built in Python, alongside client SDKs in various languages to integrate crawling flows anywhere.

## Benchmarks
High throughput with async I/O. Able to crawl 10,000+ pages per minute on standard hardware.

## Use Cases
- SEO Auditing
- Data Mining
- LLM Pre-training and RAG Dataset Generation
