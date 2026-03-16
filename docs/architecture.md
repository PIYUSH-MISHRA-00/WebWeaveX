# Architecture Overview

WebWeaveX is a monorepo designed around a clear data pipeline:

1. Discover and schedule URLs with politeness and compliance.
2. Crawl and render pages, including dynamic content.
3. Parse and extract structured content.
4. Normalize into LLM-ready documents and datasets.
5. Build semantic and knowledge graphs.
6. Expose APIs through SDKs, CLI, and plugins.

## Core Domains

- `crawler_engine/`: network runtime, fetchers, retries, and rendering
- `frontier/` and `scheduler/`: queueing, prioritization, and rate control
- `parser/` and `extractor/`: parsing and structured extraction
- `content_cleaner/`: normalization for RAG and datasets
- `semantic/`, `knowledge_graph/`, `link_graph/`: graph generation and reasoning
- `rag/`: chunking and embedding-ready dataset outputs
- `distributed/`: coordinator, workers, and queue system
- `sdk/` and `cli/`: developer-facing entry points

## Design Principles

- Compliance first: robots.txt, sitemaps, rate limits, and observability.
- Deterministic outputs: stable extraction and structured formats.
- Extensibility: plugins for strategies and extractors.
- Scalability: distributed crawling and horizontal expansion.
