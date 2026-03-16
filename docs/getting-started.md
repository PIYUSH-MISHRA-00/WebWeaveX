# Getting Started

WebWeaveX is a universal web intelligence engine that crawls the public web and turns it into
LLM-ready datasets, semantic graphs, and structured knowledge.

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Playwright and the docs site)
- Redis 5+ (for distributed crawling and benchmarks)
- spaCy model for knowledge graph extraction: `python -m spacy download en_core_web_sm`

## Install

```bash
git clone https://github.com/PIYUSH-MISHRA-00/WebWeaveX
cd WebWeaveX
python -m venv .venv
```

```bash
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
python -m pip install -e core
```

If you are running from the monorepo, add the repo root and `core/` to `PYTHONPATH` so
shared modules resolve correctly.

```bash
# Windows
set PYTHONPATH=%cd%\core;%cd%
# macOS/Linux
export PYTHONPATH="$(pwd)/core:$(pwd)"
```

## Quickstart

```bash
python cli/webweavex.py crawl https://example.com
```

```bash
python cli/webweavex.py crawl-site https://example.com
```

```bash
python cli/webweavex.py rag https://example.com
```

```bash
python cli/webweavex.py graph https://example.com
```

## Tutorials

### Crawl Tutorial

1. Pick a target site (for example, `https://docs.python.org`).
2. Run `python cli/webweavex.py crawl-site https://docs.python.org`.
3. Inspect the console output for pages crawled and metadata extracted.

### RAG Tutorial

1. Run `python cli/webweavex.py rag https://docs.python.org`.
2. Review the generated `rag_dataset.jsonl` for chunked, metadata-rich entries.
3. Import the JSONL file into your vector database of choice.

### Knowledge Graph Tutorial

1. Run `python cli/webweavex.py graph https://docs.python.org`.
2. Inspect `knowledge_graph.graphml` in a graph viewer such as Gephi or Neo4j.
3. Use the entity and relationship nodes for semantic reasoning.

## Next Steps

- Explore the architecture overview in `docs/architecture.md`.
- Review CLI reference in `docs/cli.md`.
- Browse SDK usage in `docs/sdk.md`.
