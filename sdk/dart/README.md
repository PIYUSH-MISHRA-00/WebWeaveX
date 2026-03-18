# WebWeaveX Dart SDK

## Installation
```bash
dart pub add webweavex
```

## Quick Start
```dart
import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient(
    'http://127.0.0.1:8001',
    timeout: const Duration(seconds: 10),
    maxRetries: 2,
  );
  final result = await client.crawl('https://example.com');
  print(result['status']);
  client.close();
}
```

## Usage Examples
```dart
final client = WebWeaveXClient(
  'http://127.0.0.1:8001',
  timeout: const Duration(seconds: 8),
  maxRetries: 3,
  backoffBase: const Duration(milliseconds: 400),
);

final page = await client.crawl('https://example.com');
final dataset = await client.ragDataset('https://example.com');
final graph = await client.knowledgeGraph('https://example.com');

client.close();
```

## API Reference
`WebWeaveXClient(String baseUrl, {Duration timeout, int maxRetries, Duration backoffBase, Set<int>? retryStatusCodes})`
`WebWeaveXClient(String baseUrl, {Duration timeout, int maxRetries, Duration backoffBase, Set<int>? retryStatusCodes, bool debug = false, WebWeaveXLogger? logger})`

`Future<dynamic> crawl(String url)`

`Future<dynamic> crawlSite(String url)`

`Future<dynamic> crawl_site(String url)` (alias)

`Future<dynamic> ragDataset(String url)`

`Future<dynamic> rag_dataset(String url)` (alias)

`Future<dynamic> knowledgeGraph(String url)`

`Future<dynamic> knowledge_graph(String url)` (alias)

Exceptions:

`WebWeaveXException`

`WebWeaveXTimeoutException`

`WebWeaveXNetworkException`

`WebWeaveXHttpException`

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
```dart
try {
  final result = await client.crawl('https://example.com');
  print(result['status']);
} on WebWeaveXTimeoutException {
  print('Request timed out after retries');
} on WebWeaveXHttpException catch (error) {
  print('${error.statusCode}: ${error.responseBody}');
}
```

Enable debug logging:
```dart
final client = WebWeaveXClient('http://127.0.0.1:8001', debug: true);
```

## Security Notes
- Prefer HTTPS base URLs in production.
- Validate user-provided URLs before crawl requests.
- Limit network egress from runtime environments to approved destinations only.
