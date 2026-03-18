# Repository Structure

## Folder Architecture

The repository is organized as follows:

- `ai/`: AI-powered components including crawl strategy engine and research agents.
- `assets/`: Static assets.
- `benchmarks/`: Benchmark scripts and results.
- `cli/`: Command-line interface.
- `content_cleaner/`: Content cleaning utilities.
- `core/`: Core WebWeaveX package.
- `crawler_engine/`: Site crawling engine.
- `distributed/`: Distributed crawling components (coordinator, queue, worker).
- `docs/`: Documentation.
- `examples/`: Client examples in various languages.
- `extractor/`: Content extraction pipeline.
- `frontier/`: URL frontier management.
- `knowledge_graph/`: Knowledge graph building and export.
- `link_graph/`: Link graph analysis.
- `parser/`: Parsing utilities.
- `plugins/`: Plugin system and registry.
- `rag/`: Retrieval-Augmented Generation pipeline.
- `scheduler/`: Scheduling components.
- `scripts/`: Utility scripts.
- `sdk/`: Software Development Kits for various languages.
- `semantic/`: Semantic analysis (entity and relationship extraction).
- `tests/`: Test suite.
- `website/`: Documentation website.

## Module Explanation

Each module serves a specific purpose in the WebWeaveX ecosystem:

- **Core modules** (`core/`, `crawler_engine/`, `extractor/`, etc.): Handle the fundamental crawling, fetching, content extraction, and processing.
- **AI modules** (`ai/`): Enhance crawling with intelligent strategies and semantic understanding.
- **Distributed modules** (`distributed/`): Enable scalable, multi-worker crawling using Redis queues.
- **SDKs** (`sdk/`): Provide client libraries for integration in Python, Node.js, Dart, Java, and Kotlin.
- **Plugins** (`plugins/`): Allow extensibility through a plugin interface and registry.
- **RAG and Knowledge Graph** (`rag/`, `knowledge_graph/`): Support advanced data processing for retrieval-augmented generation and graph-based knowledge representation.
- **Utilities** (`frontier/`, `scheduler/`, `semantic/`): Manage URL queues, scheduling, and semantic analysis.

## System Overview

WebWeaveX is a comprehensive web crawling and data extraction framework designed for production use. It features:

- Asynchronous crawling engine with JavaScript rendering support.
- AI-enhanced crawl strategies and semantic understanding.
- Distributed crawling capabilities for scalability.
- Multi-format output: RAG datasets, knowledge graphs, markdown, etc.
- Plugin system for extensibility.
- CLI for easy command-line usage.
- SDKs for programmatic access in multiple languages.
- Comprehensive test suite and benchmarks.

The system is built with Python as the core, using libraries like httpx, BeautifulSoup, Playwright, spaCy, and FastAPI for the API server.

## Data Flow

1. **Input**: User provides a URL via CLI, API, or SDK.
2. **Crawl Engine**: The crawler fetches pages using `httpx` and optionally Playwright for JS-rendered content.
3. **Extraction**: HTML is parsed, cleaned, and converted into structured data using extractor and content cleaner modules.
4. **Semantic Processing**: Retrieved text is analyzed with spaCy for entities and relationships.
5. **Output Generation**: Results are formatted into RAG datasets, GraphML graphs, or JSON results for SDK/API.

## Crawler Pipeline Overview

1. **URL Frontier**: Managed by `frontier/url_frontier.py` to ensure politeness and avoid duplicates.
2. **Robots & Rate Limiting**: `robots.py` and `rate_limiter.py` enforce `robots.txt` and per-domain rate limits.
3. **Fetching**: `fetcher.py` handles HTTP requests; `js_renderer.py` enables Playwright rendering for dynamic pages.
4. **Parsing**: `parser/` and `extractor/` normalize and clean HTML into consistent content models.
5. **Enrichment**: Semantic analysis adds entities and relationships, creating knowledge graph nodes.
6. **Export**: Data is output via `rag/` and `knowledge_graph/` for downstream AI/ML workflows.
