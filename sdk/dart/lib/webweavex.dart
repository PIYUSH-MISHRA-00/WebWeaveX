import 'dart:async';
import 'dart:convert';
import 'dart:io';

typedef WebWeaveXLogger = void Function(String message);

class WebWeaveXException implements Exception {
  WebWeaveXException(this.message, [this.cause]);

  final String message;
  final Object? cause;

  @override
  String toString() => 'WebWeaveXException: $message';
}

class WebWeaveXTimeoutException extends WebWeaveXException {
  WebWeaveXTimeoutException(String message, [Object? cause])
      : super(message, cause);

  @override
  String toString() => 'WebWeaveXTimeoutException: $message';
}

class WebWeaveXNetworkException extends WebWeaveXException {
  WebWeaveXNetworkException(String message, [Object? cause])
      : super(message, cause);

  @override
  String toString() => 'WebWeaveXNetworkException: $message';
}

class WebWeaveXHttpException extends WebWeaveXException {
  WebWeaveXHttpException(this.statusCode, String message, this.responseBody,
      [Object? cause])
      : super(message, cause);

  final int statusCode;
  final String responseBody;

  @override
  String toString() => 'WebWeaveXHttpException($statusCode): $message';
}

class WebWeaveXClient {
  WebWeaveXClient(
    String baseUrl, {
    this.timeout = const Duration(seconds: 10),
    int maxRetries = 2,
    Duration backoffBase = const Duration(milliseconds: 300),
    Set<int>? retryStatusCodes,
    this.debug = false,
    WebWeaveXLogger? logger,
  })  : baseUrl = baseUrl.replaceAll(RegExp(r'/$'), ''),
        _maxRetries = maxRetries < 0 ? 0 : maxRetries,
        _backoffBase = backoffBase,
        _retryStatusCodes =
            retryStatusCodes ?? const {408, 429, 500, 502, 503, 504},
        _logger = logger {
    _client.connectionTimeout = timeout;
  }

  final String baseUrl;
  final Duration timeout;
  final bool debug;
  final int _maxRetries;
  final Duration _backoffBase;
  final Set<int> _retryStatusCodes;
  final WebWeaveXLogger? _logger;
  final HttpClient _client = HttpClient();

  Future<dynamic> crawl(String url) => _post('/crawl', {'url': url});

  Future<dynamic> crawlSite(String url) => _post('/crawl_site', {'url': url});

  Future<dynamic> crawl_site(String url) => crawlSite(url);

  Future<dynamic> ragDataset(String url) => _post('/rag_dataset', {'url': url});

  Future<dynamic> rag_dataset(String url) => ragDataset(url);

  Future<dynamic> knowledgeGraph(String url) =>
      _post('/knowledge_graph', {'url': url});

  Future<dynamic> knowledge_graph(String url) => knowledgeGraph(url);

  Future<dynamic> _post(String path, Map<String, dynamic> payload) async {
    final uri = Uri.parse('$baseUrl$path');
    WebWeaveXException? lastError;

    for (var attempt = 0; attempt <= _maxRetries; attempt++) {
      final attemptNo = attempt + 1;
      _log('POST $uri attempt $attemptNo/${_maxRetries + 1}');
      try {
        final request = await _client.postUrl(uri).timeout(timeout);
        request.headers.contentType = ContentType.json;
        request.write(jsonEncode(payload));

        final response = await request.close().timeout(timeout);
        final body =
            await response.transform(utf8.decoder).join().timeout(timeout);

        if (response.statusCode < 200 || response.statusCode >= 300) {
          final httpError = WebWeaveXHttpException(
            response.statusCode,
            'Request failed with HTTP ${response.statusCode}',
            body,
          );
          lastError = httpError;
          if (_shouldRetryHttp(response.statusCode, attempt)) {
            _log(
                '${httpError.message}; retrying in ${_delayFor(attempt).inMilliseconds}ms');
            await Future<void>.delayed(_delayFor(attempt));
            continue;
          }
          throw httpError;
        }

        _log('POST $uri succeeded with HTTP ${response.statusCode}');
        try {
          return jsonDecode(body);
        } on FormatException catch (error) {
          throw WebWeaveXException('Invalid JSON response from $uri', error);
        }
      } on TimeoutException catch (error) {
        lastError =
            WebWeaveXTimeoutException('Request timed out for $uri', error);
      } on SocketException catch (error) {
        lastError =
            WebWeaveXNetworkException('Network failure for $uri', error);
      } on WebWeaveXException catch (error) {
        lastError = error;
      } catch (error) {
        lastError =
            WebWeaveXException('Unexpected error for $uri: $error', error);
      }

      if (attempt < _maxRetries) {
        _log(
            '${lastError.message}; retrying in ${_delayFor(attempt).inMilliseconds}ms');
        await Future<void>.delayed(_delayFor(attempt));
        continue;
      }

      throw lastError;
    }

    throw WebWeaveXException('Request failed for $uri');
  }

  bool _shouldRetryHttp(int statusCode, int attempt) {
    if (attempt >= _maxRetries) {
      return false;
    }
    return _retryStatusCodes.contains(statusCode);
  }

  Duration _delayFor(int attempt) {
    return Duration(
      milliseconds: _backoffBase.inMilliseconds * (1 << attempt),
    );
  }

  void close() {
    _client.close(force: true);
  }

  void _log(String message) {
    if (debug) {
      final logger = _logger ?? print;
      logger('[WebWeaveX SDK] $message');
    }
  }
}
