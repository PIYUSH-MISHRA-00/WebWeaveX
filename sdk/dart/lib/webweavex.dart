import 'dart:convert';
import 'dart:io';

class WebWeaveXClient {
  WebWeaveXClient(this.baseUrl);

  final String baseUrl;
  final HttpClient _client = HttpClient();

  Future<dynamic> crawl(String url) async {
    return _post('/crawl', {'url': url});
  }

  Future<dynamic> crawlSite(String url) async {
    return _post('/crawl_site', {'url': url});
  }

  Future<dynamic> ragDataset(String url) async {
    return _post('/rag_dataset', {'url': url});
  }

  Future<dynamic> knowledgeGraph(String url) async {
    return _post('/knowledge_graph', {'url': url});
  }

  Future<dynamic> _post(String path, Map<String, dynamic> payload) async {
    final uri = Uri.parse('${baseUrl.replaceAll(RegExp(r'/$'), '')}$path');
    final request = await _client.postUrl(uri);
    request.headers.contentType = ContentType.json;
    request.write(jsonEncode(payload));

    final response = await request.close();
    final body = await response.transform(utf8.decoder).join();
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw HttpException('Request failed: ${response.statusCode} $body', uri: uri);
    }
    return jsonDecode(body);
  }

  void close() {
    _client.close(force: true);
  }
}
