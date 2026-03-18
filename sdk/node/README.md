# WebWeaveX Node SDK

## Installation
```bash
npm install webweavex
```

## Quick Start
```js
const { WebWeaveXClient } = require("webweavex");

async function run() {
  const client = new WebWeaveXClient("http://127.0.0.1:8001", {
    timeout: 10_000,
    maxRetries: 2,
  });
  const result = await client.crawl("https://example.com");
  console.log(result.status);
}

run();
```

## Usage Examples
```js
const { WebWeaveXClient } = require("webweavex");

const client = new WebWeaveXClient("http://127.0.0.1:8001", {
  timeout: 8_000,
  maxRetries: 3,
  backoffMs: 400,
});

const page = await client.crawl("https://example.com");
const dataset = await client.ragDataset("https://example.com");
const graph = await client.knowledgeGraph("https://example.com");
```

## API Reference
`new WebWeaveXClient(baseUrl, options?)`

Options:

`timeout` (milliseconds, default `10000`)

`maxRetries` (default `2`)

`backoffMs` (default `300`)

`retryStatusCodes` (default `[408, 429, 500, 502, 503, 504]`)

`debug` (default `false`)

`logger` (custom log function)

Methods:

`crawl(url)`

`crawlSite(url)`

`crawl_site(url)` (alias)

`ragDataset(url)`

`rag_dataset(url)` (alias)

`knowledgeGraph(url)`

`knowledge_graph(url)` (alias)

Errors:

`WebWeaveXError`

`WebWeaveXTimeoutError`

`WebWeaveXNetworkError`

`WebWeaveXHTTPError`

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
```js
const {
  WebWeaveXClient,
  WebWeaveXTimeoutError,
  WebWeaveXHTTPError,
} = require("webweavex");

const client = new WebWeaveXClient("http://127.0.0.1:8001");
try {
  await client.crawl("https://example.com");
} catch (error) {
  if (error instanceof WebWeaveXTimeoutError) {
    console.error("Request timed out after retries");
  } else if (error instanceof WebWeaveXHTTPError) {
    console.error(error.statusCode, error.responseBody);
  }
}
```

Enable debug logging:
```js
const client = new WebWeaveXClient("http://127.0.0.1:8001", { debug: true });
```

## Security Notes
- Use HTTPS API URLs in production.
- Validate crawl targets before passing them into SDK methods.
- Restrict outbound network permissions for crawler workers.
