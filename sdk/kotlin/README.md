# WebWeaveX Kotlin SDK

## Installation
```xml
<dependency>
  <groupId>io.webweavex</groupId>
  <artifactId>webweavex-kotlin</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Quick Start
```kotlin
val client = WebWeaveXClient("http://127.0.0.1:8001")
val page = client.crawl("https://example.com")
println(page.status)
client.close()
```

## Usage Examples
```kotlin
val client = WebWeaveXClient(
  baseUrl = "http://127.0.0.1:8001",
  timeoutMillis = 8_000,
  maxRetries = 3,
  backoffMillis = 400,
)

val page = client.crawl("https://example.com")
val dataset = client.ragDataset("https://example.com")
val graph = client.knowledgeGraph("https://example.com")

client.close()
```

## API Reference
`WebWeaveXClient(baseUrl: String, timeoutMillis: Int = 10000, maxRetries: Int = 2, backoffMillis: Long = 300, retryStatusCodes: Set<Int> = setOf(408, 429, 500, 502, 503, 504))`

`crawl(url: String): PageResult`

`crawlSite(url: String): List<PageResult>`

`ragDataset(url: String): List<RagRecord>`

`knowledgeGraph(url: String): KnowledgeGraphResponse`

Exceptions:

`WebWeaveXException`

`WebWeaveXTimeoutException`

`WebWeaveXNetworkException`

`WebWeaveXHttpException`

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
```kotlin
try {
  client.crawl("https://example.com")
} catch (error: WebWeaveXHttpException) {
  println("${error.statusCode}: ${error.responseBody}")
}
```

## Security Notes
- Use HTTPS in production environments.
- Validate and sanitize crawl URLs before API calls.
- Restrict runtime egress permissions for crawling workloads.
