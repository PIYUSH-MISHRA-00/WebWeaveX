import '../lib/webweavex.dart';

Future<void> main() async {
  final client = WebWeaveXClient('http://localhost:8000');
  final result = await client.crawl('http://example.com');
  print(result);
  client.close();
}