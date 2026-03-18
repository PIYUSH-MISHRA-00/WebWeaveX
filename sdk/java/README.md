# WebWeaveX Java SDK

## Installation
```xml
<dependency>
  <groupId>io.webweavex</groupId>
  <artifactId>webweavex</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Quick Start
```java
WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
Map<String, Object> result = client.crawl("https://example.com");
System.out.println(result.get("status"));
```

## Usage Examples
```java
WebWeaveXClient client = new WebWeaveXClient("http://127.0.0.1:8001");
Map<String, Object> page = client.crawl("https://example.com");
List<Map<String, Object>> dataset = client.ragDataset("https://example.com");
Map<String, Object> graph = client.knowledgeGraph("https://example.com");
```

## API Reference
`WebWeaveXClient(String baseUrl)`

`Map<String, Object> crawl(String url)`

`List<Map<String, Object>> crawlSite(String url)`

`List<Map<String, Object>> ragDataset(String url)`

`Map<String, Object> knowledgeGraph(String url)`

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
Non-2xx responses throw `IOException` with status and response details. Handle with `try/catch` and add retry policy for transient network failures.

## Security Notes
Use HTTPS API endpoints, validate crawl URLs before dispatch, and run crawling workers with constrained outbound network access.
