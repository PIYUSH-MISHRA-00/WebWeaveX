# WebWeaveX

WebWeaveX is a universal web intelligence engine that turns the public web into structured knowledge, LLM-ready documents, datasets, embeddings, and semantic knowledge graphs. It is designed to be the primary knowledge ingestion engine for the Anything AI OS and a production-grade platform for developers, AI companies, and enterprises.

## Vision

- Provide a robust, extensible, and scalable web intelligence stack.
- Deliver high-quality structured data from diverse web sources with strong compliance and observability.
- Enable downstream AI workflows including RAG, dataset generation, and knowledge graphs.
- Offer consistent developer experience through SDKs, CLI, and plugins.

## Architecture Overview

WebWeaveX is organized as a monorepo with clear system boundaries:

- `crawler_engine/`: Core crawling runtime and network primitives
- `frontier/` and `scheduler/`: URL queueing, politeness, and scheduling
- `parser/`, `extractor/`, `content_cleaner/`: Content parsing and normalization
- `semantic/`, `knowledge_graph/`, `link_graph/`: Understanding and graph generation
- `rag/`: Chunking, embedding prep, and dataset export
- `ai/`: Semantic understanding and research agents
- `distributed/`: Coordinator, workers, and queue for horizontal scaling
- `sdk/`: Multi-language SDKs with identical APIs
- `cli/`: Command-line interface
- `docs/` and `website/`: Documentation and public site

## Example Usage

Python SDK (planned API):

```python
from webweavex import WebWeaveX

engine = WebWeaveX()
result = engine.crawl("https://example.com")
print(result.documents[0].text)
```

CLI:

```bash
webweavex crawl https://example.com
webweavex rag https://example.com
webweavex research "open-source vector databases"
```

## Status

Phase 1 is complete: the core Python package scaffold is in place. Implementation proceeds in incremental phases with full testing and documentation.

### Core Engine Status

- Phase 1 completed with a minimal crawler skeleton and packaging layout.
- The async engine interface is prepared and will be implemented in Phase 2.
