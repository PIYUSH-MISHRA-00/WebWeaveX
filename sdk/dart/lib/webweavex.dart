import 'dart:convert';
import 'package:http/http.dart' as http;

class WebWeaveXClient {
  WebWeaveXClient(this.baseUrl, {http.Client? client})
      : _client = client ?? http.Client();

  final String baseUrl;
  final http.Client _client;

  Future<Map<String, dynamic>> crawl(String url) async {
    return _post('/crawl', {'url': url});
  }

  Future<List<dynamic>> crawlSite(String url) async {
    return _post('/crawl_site', {'url': url});
  }

  Future<List<dynamic>> ragDataset(String url) async {
    return _post('/rag_dataset', {'url': url});
  }

  Future<Map<String, dynamic>> knowledgeGraph(String url) async {
    return _post('/knowledge_graph', {'url': url});
  }

  Future<dynamic> _post(String path, Map<String, dynamic> payload) async {
    final uri = Uri.parse(baseUrl.replaceAll(RegExp(r'\/$'), '') + path);
    final response = await _client.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception('Request failed: ${response.statusCode} ${response.body}');
    }

    return jsonDecode(response.body);
  }

  void close() {
    _client.close();
  }
}
