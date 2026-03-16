from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from webweavex.config import CrawlConfig
from webweavex.logging import get_logger

from distributed.worker.worker import Worker
from webweavex.async_engine import AsyncWebWeaveX

logger = get_logger(__name__)


def _build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="webweavex")
  subparsers = parser.add_subparsers(dest="command", required=True)

  worker_parser = subparsers.add_parser("worker", help="Start a distributed worker")
  worker_parser.add_argument("--worker-id", default="worker-1")
  worker_parser.add_argument("--redis-host", default="localhost")
  worker_parser.add_argument("--redis-port", type=int, default=6379)

  server_parser = subparsers.add_parser("server", help="Start the WebWeaveX API server")
  server_parser.add_argument("--host", default="0.0.0.0")
  server_parser.add_argument("--port", type=int, default=8000)

  crawl_parser = subparsers.add_parser("crawl", help="Crawl a single page")
  crawl_parser.add_argument("url")

  crawl_site_parser = subparsers.add_parser("crawl-site", help="Crawl an entire site")
  crawl_site_parser.add_argument("url")

  rag_parser = subparsers.add_parser("rag", help="Build a RAG dataset from a site")
  rag_parser.add_argument("url")
  rag_parser.add_argument("--output", default="rag_dataset.jsonl")

  graph_parser = subparsers.add_parser("graph", help="Build a knowledge graph from a site")
  graph_parser.add_argument("url")
  graph_parser.add_argument("--output", default="knowledge_graph.graphml")

  plugins_parser = subparsers.add_parser("plugins", help="Manage plugin registry")
  plugins_subparsers = plugins_parser.add_subparsers(dest="plugins_command", required=True)
  plugins_list_parser = plugins_subparsers.add_parser("list", help="List available plugins")
  plugins_list_parser.add_argument("--registry", default="plugins/registry/registry.json")

  return parser


async def _run_crawl(url: str) -> None:
  async with AsyncWebWeaveX() as engine:
    result = await engine.crawl(url)
  print(json.dumps(result.model_dump(), indent=2))


async def _run_crawl_site(url: str) -> None:
  async with AsyncWebWeaveX() as engine:
    pages = await engine.crawl_site(url)
  print(f"Pages crawled: {len(pages)}")


async def _run_rag(url: str, output: str) -> None:
  from rag.dataset_builder.exporter import export_jsonl

  async with AsyncWebWeaveX() as engine:
    dataset = await engine.build_rag_dataset(url)
  export_jsonl(dataset, Path(output))
  print(f"RAG dataset saved to {output}")


async def _run_graph(url: str, output: str) -> None:
  from knowledge_graph.exporter import export_graphml

  async with AsyncWebWeaveX() as engine:
    graph = await engine.build_knowledge_graph(url)
  export_graphml(graph, Path(output))
  print(f"Knowledge graph saved to {output}")


def _run_plugins_list(registry_path: str) -> None:
  path = Path(registry_path)
  if not path.exists():
    print(f"Plugin registry not found at {registry_path}")
    return

  data = json.loads(path.read_text(encoding="utf-8"))
  plugins = data.get("plugins", [])
  if not plugins:
    print("No plugins registered")
    return

  print("Available plugins:")
  for plugin in plugins:
    name = plugin.get("name", "unknown")
    description = plugin.get("description", "")
    author = plugin.get("author", "unknown")
    version = plugin.get("version", "unknown")
    print(f"- {name} ({version}) by {author} - {description}")


def main() -> None:
  parser = _build_parser()
  args = parser.parse_args()

  if args.command == "worker":
    config = CrawlConfig(
      worker_id=args.worker_id,
      redis_host=args.redis_host,
      redis_port=args.redis_port,
    )
    worker = Worker(config)
    logger.info("Starting worker %s", config.worker_id)
    asyncio.run(worker.run())

  elif args.command == "server":
    from webweavex.api_server import app
    import uvicorn

    logger.info("Starting API server on %s:%s", args.host, args.port)
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

  elif args.command == "crawl":
    asyncio.run(_run_crawl(args.url))

  elif args.command == "crawl-site":
    asyncio.run(_run_crawl_site(args.url))

  elif args.command == "rag":
    asyncio.run(_run_rag(args.url, args.output))

  elif args.command == "graph":
    asyncio.run(_run_graph(args.url, args.output))

  elif args.command == "plugins":
    if args.plugins_command == "list":
      _run_plugins_list(args.registry)


if __name__ == "__main__":
  main()
