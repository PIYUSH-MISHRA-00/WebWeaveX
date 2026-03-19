# WebWeaveX Kotlin SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.piyush-mishra-00/webweavex-kotlin?label=Maven%20Central)](https://central.sonatype.com/artifact/io.github.piyush-mishra-00/webweavex-kotlin)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](../../LICENSE)

Kotlin SDK for [WebWeaveX](https://github.com/PIYUSH-MISHRA-00/WebWeaveX) — AI-native web crawling with coroutine support.

## Version

`0.1.0` · Kotlin 1.9.24 · Java 11+ · Maven Central

## Installation

### Gradle Kotlin DSL
```kotlin
implementation("io.github.piyush-mishra-00:webweavex-kotlin:0.1.0")
```

### Maven
```xml
<dependency>
  <groupId>io.github.piyush-mishra-00</groupId>
  <artifactId>webweavex-kotlin</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Quick Start

```kotlin
import io.github.piyushmishra.webweavex.WebWeaveX
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val client = WebWeaveX.create {
        baseUrl = "http://localhost:8001"
        retries = 3
        debug   = true
    }

    // Crawl a single page
    val page = client.crawl("https://example.com")
    println(page["status"])

    // RAG dataset
    val rag = client.rag("https://example.com")
    println(rag["records"])

    // Knowledge graph
    val graph = client.graph("https://example.com")
    println(graph["nodes"])

    client.close()
}
```

## API Reference

| Method | Endpoint | Return type |
|---|---|---|
| `crawl(url)` | `/crawl` | `Map<String, Any>` |
| `rag(url)` | `/rag_dataset` | `Map<String, Any>` |
| `graph(url)` | `/knowledge_graph` | `Map<String, Any>` |

### `WebWeaveX.create { }` options

| Option | Type | Default | Description |
|---|---|---|---|
| `baseUrl` | `String` | `"http://localhost:8001"` | API server base URL |
| `retries` | `Int` | `3` | Max retry attempts |
| `backoffMillis` | `Long` | `300` | Base backoff delay (ms) |
| `debug` | `Boolean` | `false` | Enable debug logging |

## Error Handling

```kotlin
import io.github.piyushmishra.webweavex.WebWeaveX
import kotlinx.coroutines.runBlocking

runBlocking {
    val client = WebWeaveX.create { baseUrl = "http://localhost:8001" }
    try {
        val result = client.crawl("https://example.com")
    } catch (e: Exception) {
        println("Error: ${e.message}")
    }
}
```

## License

Apache-2.0
