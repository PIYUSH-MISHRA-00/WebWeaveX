import '../sdk/dart/lib/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient('http://localhost:8000');
  final result = await client.crawl('https://example.com');
  print(result);
  client.close();
}
