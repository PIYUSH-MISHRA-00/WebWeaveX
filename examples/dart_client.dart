import '../sdk/dart/lib/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient('http://127.0.0.1:8001');
  final result = await client.crawl('https://example.com');

  print('Dart SDK test passed');
  print('Status: ${result['status']}');
  print('URL: ${result['url']}');
  print('Title: ${result['metadata']['title']}');

  client.close();
}
