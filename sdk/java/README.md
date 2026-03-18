# WebWeaveX Java SDK

## Installation
```xml
<dependency>
  <groupId>io.webweavex</groupId>
  <artifactId>webweavex-java</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Quick Start
```java
WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
WebWeaveXClient.PageResult page = client.crawl("https://example.com");
System.out.println(page.status);
```

## Usage Examples
```java
WebWeaveXClient client = new WebWeaveXClient(
    "http://127.0.0.1:8001",
    8000,   // timeoutMillis
    3,      // maxRetries
    400,    // backoffMillis
    Set.of(408, 429, 500, 502, 503, 504)
);

WebWeaveXClient.PageResult page = client.crawl("https://example.com");
List<WebWeaveXClient.RagRecord> dataset = client.ragDataset("https://example.com");
WebWeaveXClient.KnowledgeGraphResponse graph = client.knowledgeGraph("https://example.com");
```

## API Reference
`WebWeaveXClient(String baseUrl)`

`WebWeaveXClient(String baseUrl, int timeoutMillis, int maxRetries, int backoffMillis, Set<Integer> retryStatuses)`

`PageResult crawl(String url)`

`List<PageResult> crawlSite(String url)`

`List<RagRecord> ragDataset(String url)`

`KnowledgeGraphResponse knowledgeGraph(String url)`

Exceptions:

`WebWeaveXClient.WebWeaveXException`

`WebWeaveXClient.WebWeaveXTimeoutException`

`WebWeaveXClient.WebWeaveXNetworkException`

`WebWeaveXClient.WebWeaveXHTTPException`

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
```java
try {
  client.crawl("https://example.com");
} catch (WebWeaveXClient.WebWeaveXHTTPException error) {
  System.out.println(error.getStatusCode());
  System.out.println(error.getResponseBody());
}
```

## Security Notes
- Use HTTPS endpoints in production.
- Validate crawl targets before submitting requests.
- Run crawler clients and workers with restricted network access policies.
