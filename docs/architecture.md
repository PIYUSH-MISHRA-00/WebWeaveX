# Architecture Overview

WebWeaveX is a monorepo designed around a clear data pipeline that turns the web into
structured knowledge for AI systems.

## End-to-End Flow

1. Discover and schedule URLs with politeness and compliance.
2. Crawl and render pages, including dynamic content.
3. Parse and extract structured content.
4. Normalize into LLM-ready documents and datasets.
5. Build semantic and knowledge graphs.
6. Expose APIs through SDKs, CLI, and plugins.

## Core Domains

- `crawler_engine/`: crawl orchestration, site crawling, and link discovery
- `frontier/` and `scheduler/`: queueing, prioritization, and rate control
- `parser/` and `extractor/`: parsing and structured extraction
- `content_cleaner/`: normalization for RAG and datasets
- `semantic/`, `knowledge_graph/`, `link_graph/`: graph generation and reasoning
- `rag/`: chunking and embedding-ready dataset outputs
- `distributed/`: coordinator, workers, and queue system
- `sdk/` and `cli/`: developer-facing entry points

## Runtime Components

- `AsyncWebWeaveX`: concurrent engine for crawl, RAG, and knowledge graph pipelines.
- `AsyncCrawler`: core async fetch and parse flow with robots and JS rendering support.
- `SiteCrawler`: frontier-driven site traversal with depth and domain policies.
- `JSRenderer`: optional Playwright rendering for dynamic pages.
- `RobotsHandler` + `SitemapDiscoverer`: compliance and crawl politeness helpers.

## Plugin System

Plugins allow teams to extend extraction and post-processing without modifying core code.
WebWeaveX scans the `plugins/` directory at runtime and registers any modules exposing
`WebWeaveXPlugin` implementations. After core extraction runs, matching plugins can
enrich `PageResult` objects with domain-specific metadata (for example, YouTube video
details).

## Design Principles

- Compliance first: robots.txt, sitemaps, rate limits, and observability.
- Deterministic outputs: stable extraction and structured formats.
- Extensibility: plugins for strategies and extractors.
- Scalability: distributed crawling and horizontal expansion.
