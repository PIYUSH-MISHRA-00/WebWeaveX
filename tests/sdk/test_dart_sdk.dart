// Dart SDK integration tests
import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('Dart SDK crawl test', () async {
    final client = WebWeaveXClient('http://127.0.0.1:8001');
    
    try {
      // Test crawl
      final result = await client.crawl('http://example.com');
      
      // Validate response
      expect(result['status'], equals(200));
      print('✅ Dart SDK crawl test passed');
      
      // Validate JSON structure
      expect(result, contains('html'));
      expect(result, contains('metadata'));
      expect(result, contains('url'));
      print('✅ Dart SDK response structure validated');
      
      // Test JSON parsing
      expect(result, isA<Map>());
      print('✅ Dart SDK response is valid JSON object');
      
      client.close();
    } catch (error) {
      client.close();
      rethrow;
    }
  });
}
