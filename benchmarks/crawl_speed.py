from __future__ import annotations

import argparse
import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from webweavex.async_engine import AsyncWebWeaveX
from webweavex.config import CrawlConfig
from webweavex.logging import get_logger

logger = get_logger(__name__)

DEFAULT_TARGETS = [
  "https://example.com",
  "https://docs.python.org",
]


async def _benchmark_target(url: str, config: CrawlConfig) -> dict[str, object]:
  logger.info("Benchmark crawl for %s", url)
  start = time.perf_counter()
  pages_crawled = 0
  error = None
  try:
    async with AsyncWebWeaveX(config) as engine:
      pages = await engine.crawl_site(url)
      pages_crawled = len(pages)
  except Exception as exc:
    error = str(exc)
  elapsed = time.perf_counter() - start
  pages_per_second = pages_crawled / elapsed if elapsed > 0 else 0.0
  return {
    "url": url,
    "pages_crawled": pages_crawled,
    "crawl_time_seconds": round(elapsed, 4),
    "pages_per_second": round(pages_per_second, 4),
    "error": error,
  }


async def run_benchmark(
  targets: list[str],
  max_pages: int,
  max_depth: int,
  output_path: Path,
) -> dict[str, object]:
  config = CrawlConfig(max_pages=max_pages, max_depth=max_depth)
  results = []
  total_pages = 0
  total_time = 0.0

  for target in targets:
    result = await _benchmark_target(target, config)
    results.append(result)
    total_pages += int(result.get("pages_crawled", 0))
    total_time += float(result.get("crawl_time_seconds", 0.0))

  total_pages_per_second = total_pages / total_time if total_time > 0 else 0.0
  payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "config": {
      "max_pages": max_pages,
      "max_depth": max_depth,
    },
    "targets": results,
    "total_pages": total_pages,
    "total_time_seconds": round(total_time, 4),
    "total_pages_per_second": round(total_pages_per_second, 4),
  }

  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
  logger.info("Crawl speed results saved to %s", output_path)
  return payload


def main() -> None:
  parser = argparse.ArgumentParser(description="Benchmark WebWeaveX crawl speed")
  parser.add_argument("--max-pages", type=int, default=20)
  parser.add_argument("--max-depth", type=int, default=2)
  parser.add_argument("--output", default=str(Path("benchmarks/results/crawl_speed.json")))
  parser.add_argument("targets", nargs="*", default=DEFAULT_TARGETS)
  args = parser.parse_args()

  output_path = Path(args.output)
  asyncio.run(run_benchmark(args.targets, args.max_pages, args.max_depth, output_path))


if __name__ == "__main__":
  main()
