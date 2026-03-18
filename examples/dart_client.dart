import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> main() async {
  final response = await http.post(
    Uri.parse('http://127.0.0.1:8001/crawl'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'url': 'https://example.com'}),
  );

  final result = jsonDecode(response.body);
  print('✅ Dart SDK test passed');
  print('Status: ${result['status']}');
  print('URL: ${result['url']}');
  print('Title: ${result['metadata']['title']}');
}
