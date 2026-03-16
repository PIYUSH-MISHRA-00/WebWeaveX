# CLI

The WebWeaveX CLI provides a simple entry point for crawling, RAG preparation, and knowledge graph workflows.

## Commands

- `webweavex crawl <url>`
- `webweavex crawl-site <url>`
- `webweavex rag <url>`
- `webweavex graph <url>`
- `webweavex worker`
- `webweavex server`

## Examples

```bash
webweavex crawl https://example.com
```

```bash
webweavex crawl-site https://example.com
```

```bash
webweavex rag https://example.com
```

```bash
webweavex graph https://example.com
```

```bash
webweavex worker
```

```bash
webweavex server
```

## Outputs

- `webweavex crawl` prints JSON to stdout.
- `webweavex crawl-site` prints the number of pages crawled.
- `webweavex rag` writes `rag_dataset.jsonl`.
- `webweavex graph` writes `knowledge_graph.graphml`.

## Output Philosophy

- Human-readable progress logs
- Structured artifacts saved to disk
- Clear exit codes for automation
