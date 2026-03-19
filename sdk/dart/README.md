# WebWeaveX Dart SDK

[![pub.dev](https://img.shields.io/pub/v/webweavex?label=pub.dev)](https://pub.dev/packages/webweavex)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](../../LICENSE)

Dart SDK for [WebWeaveX](https://github.com/PIYUSH-MISHRA-00/WebWeaveX) — async web crawling client using `dart:io`'s `HttpClient`.

## Version

`0.1.1` · Dart SDK ≥2.17.0 \<4.0.0 · pub.dev

## Installation

```bash
dart pub add webweavex
```

Or add to `pubspec.yaml`:

```yaml
dependencies:
  webweavex: ^0.1.1
```

## Quick Start

```dart
import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient(
    'http://localhost:8001',
    maxRetries: 2,
    debug: false,
  );

  // Crawl a single page
  final page = await client.crawl('https://example.com');
  print(page['status']);           // 200

  // Generate RAG dataset
  final records = await client.ragDataset('https://example.com');
  print('${(records as List).length} chunks');

  // Extract knowledge graph
  final kg = await client.knowledgeGraph('https://example.com');
  print('${(kg['nodes'] as List).length} nodes');

  client.close();
}
```

## API Reference

| Method | Endpoint | Returns |
|---|---|---|
| `crawl(url)` | `/crawl` | `Future<dynamic>` |
| `crawlSite(url)` | `/crawl_site` | `Future<dynamic>` |
| `ragDataset(url)` | `/rag_dataset` | `Future<dynamic>` |
| `knowledgeGraph(url)` | `/knowledge_graph` | `Future<dynamic>` |

> **Note:** snake_case aliases (`crawl_site`, `rag_dataset`, `knowledge_graph`) are also available.

### Constructor Options

```dart
WebWeaveXClient(
  'http://localhost:8001',
  timeout: Duration(seconds: 10),
  maxRetries: 2,
  backoffBase: Duration(milliseconds: 300),
  retryStatusCodes: {408, 429, 500, 502, 503, 504},
  debug: false,
  logger: null,    // custom void Function(String) logger
)
```

## Error Types

| Class | Cause |
|---|---|
| `WebWeaveXException` | Base SDK exception |
| `WebWeaveXTimeoutException` | Request timed out |
| `WebWeaveXNetworkException` | Network/connection failure |
| `WebWeaveXHttpException` | Non-2xx HTTP response (`.statusCode`, `.responseBody`) |

## License

Apache-2.0
