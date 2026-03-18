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
val result = client.crawl("https://example.com")
println(result)
```

## Usage Examples
```kotlin
val client = WebWeaveXClient("http://127.0.0.1:8001")
val page = client.crawl("https://example.com")
val dataset = client.ragDataset("https://example.com")
val graph = client.knowledgeGraph("https://example.com")
```

## API Reference
`WebWeaveXClient(baseUrl: String)`

`crawl(url: String): String`

`crawlSite(url: String): String`

`ragDataset(url: String): String`

`knowledgeGraph(url: String): String`

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
SDK calls throw `IOException` when the API returns non-2xx responses. Wrap calls with `try/catch` and inspect returned status details.

## Security Notes
Use HTTPS for production endpoints, enforce URL allowlists for crawl jobs, and run agents in restricted network contexts.
