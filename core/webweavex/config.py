from dataclasses import dataclass, field
import os

DEFAULT_HEADERS: dict[str, str] = {
  "User-Agent": "WebWeaveX/0.1 (+https://github.com/PIYUSH-MISHRA-00/WebWeaveX)"
}


@dataclass(frozen=True)
class CrawlConfig:
  """Configuration for crawling and fetching."""

  timeout: float = 10.0
  connect_timeout: float | None = None
  read_timeout: float | None = None
  write_timeout: float | None = None
  pool_timeout: float | None = None
  headers: dict[str, str] = field(default_factory=lambda: DEFAULT_HEADERS.copy())
  retries: int = 2
  retry_backoff_base: float = 0.5
  retry_backoff_max: float = 8.0
  rate_limit_per_second: float = 5.0
  enable_js: bool = False
  js_wait_time: float = 2.0
  js_wait_for_selector: str | None = None
  js_headless: bool = True
  max_concurrency: int = 10
  max_pages: int = 100
  max_depth: int = 3
  allowed_domains: list[str] | None = None
  enable_ai_strategy: bool = False
  strategy_keywords: list[str] = field(
    default_factory=lambda: ["docs", "api", "guide", "reference", "tutorial"]
  )
  worker_id: str = "worker-1"
  redis_host: str = "localhost"
  redis_port: int = 6379

  # SSL verification for HTTPS requests.
  # - True: use system certificate store (default, recommended)
  # - False: disable verification (INSECURE - testing only)
  # - str: path to custom CA bundle file
  ssl_verify: bool | str = True
