# WebWeaveX Benchmarks Report

**Updated**: March 18, 2026

## Baseline Validation

| Target | Endpoint | Result |
| --- | --- | --- |
| `https://example.com` | CLI `crawl` | `200 OK` |
| `https://example.com` | API `/crawl` | `200 OK` |
| `https://example.com` | SDK samples (all languages) | `200 OK` |

## Benchmark Scripts

| Script | Purpose |
| --- | --- |
| `benchmarks/crawl_speed.py` | Request latency and throughput checks |
| `benchmarks/distributed_scaling.py` | Multi-worker scaling behavior |
| `benchmarks/js_rendering.py` | JavaScript rendering overhead |

## Notes

- Results depend on network conditions and target site complexity.
- Use production-like infrastructure for comparative benchmarking.
- Save benchmark runs under `benchmarks/results/` for longitudinal tracking.
