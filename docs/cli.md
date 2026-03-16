# CLI

The WebWeaveX CLI provides a simple entry point for crawling, RAG preparation, and knowledge graph workflows.

## Commands

- `webweavex crawl <url>`
- `webweavex crawl-site <url>`
- `webweavex rag <url>`
- `webweavex graph <url>`
- `webweavex repo <github-url>`
- `webweavex plugins list`
- `webweavex worker`
- `webweavex server`

## Examples

```bash
webweavex --help
```

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
webweavex repo https://github.com/user/repo
```

```bash
webweavex plugins list
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
- `webweavex repo` writes `repo_dataset.jsonl`, `repo_graph.graphml`, and `repo_summary.md`.

## Output Philosophy

- Human-readable progress logs
- Structured artifacts saved to disk
- Clear exit codes for automation
