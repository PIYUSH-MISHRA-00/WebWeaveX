# WebWeaveX Node SDK

## Installation
```bash
npm install webweavex
```

## Quick Start
```js
const { WebWeaveXClient } = require("webweavex");

async function run() {
  const client = new WebWeaveXClient("http://127.0.0.1:8001");
  const result = await client.crawl("https://example.com");
  console.log(result.status);
}

run();
```

## Usage Examples
```js
const client = new WebWeaveXClient("http://127.0.0.1:8001");
const page = await client.crawl("https://example.com");
const dataset = await client.ragDataset("https://example.com");
const graph = await client.knowledgeGraph("https://example.com");
```

## API Reference
`new WebWeaveXClient(baseUrl)`

`crawl(url)`

`crawlSite(url)`

`ragDataset(url)`

`knowledgeGraph(url)`

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
All methods throw `Error` when request transport fails or an HTTP status is non-2xx. Wrap calls in `try/catch` and implement retries for transient failures.

## Security Notes
Use HTTPS API URLs in production, apply outbound request allowlists for crawl targets, and sanitize user-provided URLs before invoking SDK calls.
