from __future__ import annotations

import argparse
import asyncio

from webweavex.config import CrawlConfig
from webweavex.logging import get_logger

from distributed.worker.worker import Worker

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

  return parser


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


if __name__ == "__main__":
  main()
