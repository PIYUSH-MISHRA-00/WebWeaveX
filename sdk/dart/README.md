# WebWeaveX Dart SDK

## Installation
```bash
dart pub add webweavex
```

## Quick Start
```dart
import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient('http://127.0.0.1:8001');
  final result = await client.crawl('https://example.com');
  print(result['status']);
  client.close();
}
```

## Usage Examples
```dart
final client = WebWeaveXClient('http://127.0.0.1:8001');
final page = await client.crawl('https://example.com');
final dataset = await client.ragDataset('https://example.com');
final graph = await client.knowledgeGraph('https://example.com');
client.close();
```

## API Reference
`WebWeaveXClient(String baseUrl)`

`Future<dynamic> crawl(String url)`

`Future<dynamic> crawlSite(String url)`

`Future<dynamic> ragDataset(String url)`

`Future<dynamic> knowledgeGraph(String url)`

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
SDK methods throw `HttpException` for non-2xx responses. Use `try/catch` around calls and inspect status/body values when handling failures.

## Security Notes
Use HTTPS base URLs for production, restrict crawl targets by policy, and avoid processing untrusted URLs without validation.
