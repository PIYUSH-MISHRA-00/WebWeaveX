# WebWeaveX Node.js SDK

[![npm](https://img.shields.io/npm/v/webweavex?label=npm)](https://www.npmjs.com/package/webweavex)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](../../LICENSE)

Node.js SDK for [WebWeaveX](https://github.com/PIYUSH-MISHRA-00/WebWeaveX) — async web crawling client with full retry + backoff support.

## Version

`0.1.0` · Node.js 18+ · npm

## Installation

```bash
npm install webweavex
```

## Quick Start

```js
const { WebWeaveXClient } = require("webweavex");

const client = new WebWeaveXClient("http://localhost:8001");

// Crawl a single page
const page = await client.crawl("https://example.com");
console.log(page.status);           // 200
console.log(page.metadata.title);

// Generate RAG dataset
const records = await client.ragDataset("https://example.com");
console.log(records.length, "chunks");

// Extract knowledge graph
const kg = await client.knowledgeGraph("https://example.com");
console.log(kg.nodes.length, "nodes");
```

## API Reference

| Method | Endpoint | Returns |
|---|---|---|
| `crawl(url)` | `/crawl` | `Promise<object>` |
| `crawlSite(url)` | `/crawl_site` | `Promise<object[]>` |
| `ragDataset(url)` | `/rag_dataset` | `Promise<object[]>` |
| `knowledgeGraph(url)` | `/knowledge_graph` | `Promise<object>` |

> **Note:** snake_case aliases (`crawl_site`, `rag_dataset`, `knowledge_graph`) are also available.

### Constructor Options

```js
new WebWeaveXClient("http://localhost:8001", {
  timeout: 10_000,          // ms
  maxRetries: 2,
  backoffMs: 300,
  retryStatusCodes: [408, 429, 500, 502, 503, 504],
  debug: false,
  logger: null,             // custom (msg) => void logger
})
```

## Error Types

| Class | Cause |
|---|---|
| `WebWeaveXError` | Base SDK error |
| `WebWeaveXTimeoutError` | Request timed out |
| `WebWeaveXHTTPError` | Non-2xx HTTP response (`.statusCode`, `.responseBody`) |
| `WebWeaveXNetworkError` | Network/connection failure |

## License

Apache-2.0
