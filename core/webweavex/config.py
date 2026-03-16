from dataclasses import dataclass, field

DEFAULT_HEADERS: dict[str, str] = {
  "User-Agent": "WebWeaveX/0.1 (+https://github.com/PIYUSH-MISHRA-00/WebWeaveX)"
}


@dataclass(frozen=True)
class CrawlConfig:
  """Configuration for crawling and fetching."""

  timeout: float = 10.0
  headers: dict[str, str] = field(default_factory=lambda: DEFAULT_HEADERS.copy())
  retries: int = 2
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
