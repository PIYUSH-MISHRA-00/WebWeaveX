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


async def _measure(url: str, enable_js: bool) -> dict[str, object]:
  config = CrawlConfig(enable_js=enable_js)
  label = "rendered" if enable_js else "non_rendered"
  start = time.perf_counter()
  status = "ok"
  error = None
  try:
    async with AsyncWebWeaveX(config) as engine:
      await engine.crawl(url)
  except Exception as exc:
    status = "error"
    error = str(exc)
  elapsed = time.perf_counter() - start
  logger.info("%s crawl for %s took %.4fs", label, url, elapsed)
  return {
    "time_seconds": round(elapsed, 4),
    "status": status,
    "error": error,
  }


async def run_benchmark(targets: list[str], output_path: Path) -> dict[str, object]:
  results = []
  for url in targets:
    non_rendered = await _measure(url, enable_js=False)
    rendered = await _measure(url, enable_js=True)
    slowdown = None
    if non_rendered["time_seconds"] and rendered["time_seconds"]:
      slowdown = round(rendered["time_seconds"] / non_rendered["time_seconds"], 4)
    results.append(
      {
        "url": url,
        "non_rendered": non_rendered,
        "rendered": rendered,
        "slowdown_factor": slowdown,
      }
    )

  payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "targets": results,
  }

  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
  logger.info("JS rendering results saved to %s", output_path)
  return payload


def main() -> None:
  parser = argparse.ArgumentParser(description="Benchmark JS rendering performance")
  parser.add_argument("--output", default=str(Path("benchmarks/results/js_rendering.json")))
  parser.add_argument("targets", nargs="*", default=DEFAULT_TARGETS)
  args = parser.parse_args()

  output_path = Path(args.output)
  asyncio.run(run_benchmark(args.targets, output_path))


if __name__ == "__main__":
  main()
