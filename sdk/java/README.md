# WebWeaveX Java SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.piyush-mishra-00/webweavex?label=Maven%20Central)](https://central.sonatype.com/artifact/io.github.piyush-mishra-00/webweavex)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](../../LICENSE)

Java SDK for [WebWeaveX](https://github.com/PIYUSH-MISHRA-00/WebWeaveX) — typed, production-ready web crawling client.

## Version

`0.1.0` · Java 8+ · Maven Central

## Installation

### Maven
```xml
<dependency>
  <groupId>io.github.piyush-mishra-00</groupId>
  <artifactId>webweavex</artifactId>
  <version>0.1.0</version>
</dependency>
```

### Gradle
```groovy
implementation 'io.github.piyush-mishra-00:webweavex:0.1.0'
```

## Quick Start

```java
import io.github.piyushmishra.webweavex.WebWeaveXClient;
import io.github.piyushmishra.webweavex.PageResult;
import io.github.piyushmishra.webweavex.KnowledgeGraphResponse;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        var client = new WebWeaveXClient("http://localhost:8001");

        // Crawl a single page
        PageResult page = client.crawl("https://example.com");
        System.out.println("Status: " + page.getStatus());

        // Crawl entire site
        List<PageResult> pages = client.crawlSite("https://example.com");
        System.out.println("Pages: " + pages.size());

        // Knowledge graph
        KnowledgeGraphResponse kg = client.knowledgeGraph("https://example.com");
        System.out.println("Nodes: " + kg.getNodes().size());
    }
}
```

## API Reference

| Method | Endpoint | Return type |
|---|---|---|
| `crawl(url)` | `/crawl` | `PageResult` |
| `crawlSite(url)` | `/crawl_site` | `List<PageResult>` |
| `ragDataset(url)` | `/rag_dataset` | `List<RagRecord>` |
| `knowledgeGraph(url)` | `/knowledge_graph` | `KnowledgeGraphResponse` |

### Constructor Options

```java
new WebWeaveXClient(
    "http://localhost:8001",  // baseUrl
    10_000,                   // timeoutMillis
    2,                        // maxRetries
    300L,                     // backoffMillis
    Set.of(429,500,502,503),  // retryStatusCodes
    false,                    // debug
    System.out::println       // logger
);
```

## Error Types

| Exception | Cause |
|---|---|
| `WebWeaveXException` | Base SDK exception |
| `WebWeaveXTimeoutException` | Request timed out |
| `WebWeaveXNetworkException` | Network/connection failure |
| `WebWeaveXHttpException` | Non-2xx HTTP response |

## License

Apache-2.0
