from __future__ import annotations

import argparse
import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import redis

from distributed.queue.redis_queue import RedisQueue
from webweavex.async_engine import AsyncWebWeaveX
from webweavex.config import CrawlConfig
from webweavex.logging import get_logger

logger = get_logger(__name__)

DEFAULT_TARGETS = [
  "https://example.com",
  "https://docs.python.org/3/",
]

WORKER_COUNTS = [1, 2, 4, 8]


def _p95(values: list[float]) -> float:
  if not values:
    return 0.0
  values_sorted = sorted(values)
  index = int(0.95 * (len(values_sorted) - 1))
  return values_sorted[index]


async def _worker_loop(
  worker_id: str,
  queue: RedisQueue,
  engine: AsyncWebWeaveX,
  total_jobs: int,
  metrics: dict[str, object],
  lock: asyncio.Lock,
  done: asyncio.Event,
) -> None:
  while not done.is_set():
    payload = await asyncio.to_thread(queue.dequeue, 1)
    if payload is None:
      continue
    try:
      job = json.loads(payload)
    except json.JSONDecodeError:
      continue

    url = job.get("url")
    enqueued_at = job.get("enqueued_at")
    if not url:
      continue

    dequeue_time = time.perf_counter()
    if enqueued_at is not None:
      queue_latency = dequeue_time - float(enqueued_at)
    else:
      queue_latency = 0.0

    await engine.crawl(url)

    async with lock:
      metrics["processed"] = int(metrics["processed"]) + 1
      metrics["queue_latencies"].append(queue_latency)
      per_worker = metrics["per_worker"]
      per_worker[worker_id] = per_worker.get(worker_id, 0) + 1
      if int(metrics["processed"]) >= total_jobs:
        done.set()


async def _run_once(
  worker_count: int,
  queue: RedisQueue,
  target_urls: list[str],
  total_jobs: int,
) -> dict[str, object]:
  logger.info("Distributed scaling run with %s workers", worker_count)
  metrics: dict[str, object] = {
    "processed": 0,
    "queue_latencies": [],
    "per_worker": {},
  }
  lock = asyncio.Lock()
  done = asyncio.Event()

  config = CrawlConfig(max_concurrency=5)
  engines = [AsyncWebWeaveX(config) for _ in range(worker_count)]

  tasks = []
  for idx in range(worker_count):
    worker_id = f"worker-{idx + 1}"
    tasks.append(
      asyncio.create_task(
        _worker_loop(worker_id, queue, engines[idx], total_jobs, metrics, lock, done)
      )
    )

  start = time.perf_counter()
  await done.wait()
  duration = time.perf_counter() - start

  for task in tasks:
    task.cancel()
  await asyncio.gather(*tasks, return_exceptions=True)

  for engine in engines:
    await engine.aclose()

  processed = int(metrics["processed"])
  throughput = processed / duration if duration > 0 else 0.0
  latencies = metrics["queue_latencies"]
  avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

  return {
    "workers": worker_count,
    "jobs": total_jobs,
    "duration_seconds": round(duration, 4),
    "throughput_per_second": round(throughput, 4),
    "queue_latency_seconds_avg": round(avg_latency, 4),
    "queue_latency_seconds_p95": round(_p95(latencies), 4),
    "per_worker": metrics["per_worker"],
  }


def _build_jobs(targets: list[str], total_jobs: int) -> list[str]:
  jobs: list[str] = []
  for idx in range(total_jobs):
    url = targets[idx % len(targets)]
    payload = {
      "id": idx,
      "url": url,
      "enqueued_at": time.perf_counter(),
    }
    jobs.append(json.dumps(payload))
  return jobs


def main() -> None:
  parser = argparse.ArgumentParser(description="Benchmark distributed scaling")
  parser.add_argument("--redis-host", default="localhost")
  parser.add_argument("--redis-port", type=int, default=6379)
  parser.add_argument("--queue", default="webweavex:bench")
  parser.add_argument("--jobs", type=int, default=20)
  parser.add_argument("--output", default=str(Path("benchmarks/results/distributed_scaling.json")))
  parser.add_argument("targets", nargs="*", default=DEFAULT_TARGETS)
  args = parser.parse_args()

  output_path = Path(args.output)
  output_path.parent.mkdir(parents=True, exist_ok=True)

  client = redis.Redis(host=args.redis_host, port=args.redis_port, decode_responses=True)
  try:
    client.ping()
  except Exception as exc:
    payload = {
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "error": f"Redis not available: {exc}",
      "runs": [],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.warning("Redis unavailable, skipping benchmark")
    return

  queue = RedisQueue(host=args.redis_host, port=args.redis_port, name=args.queue, client=client)

  runs = []
  for worker_count in WORKER_COUNTS:
    client.delete(args.queue)
    jobs = _build_jobs(args.targets, args.jobs)
    for job in jobs:
      queue.enqueue(job)

    result = asyncio.run(_run_once(worker_count, queue, args.targets, args.jobs))
    runs.append(result)

  payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "queue": {
      "host": args.redis_host,
      "port": args.redis_port,
      "name": args.queue,
    },
    "targets": args.targets,
    "jobs": args.jobs,
    "runs": runs,
  }

  output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
  logger.info("Distributed scaling results saved to %s", output_path)


if __name__ == "__main__":
  main()
