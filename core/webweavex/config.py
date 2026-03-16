from dataclasses import dataclass, field

DEFAULT_HEADERS: dict[str, str] = {
  "User-Agent": "WebWeaveX/0.1 (+https://github.com/PIYUSH-MISHRA-00/WebWeaveX)"
}


@dataclass(frozen=True)
class CrawlConfig:
  """Configuration for crawling and fetching.

  enable_js is reserved for future Playwright rendering support.
  """

  timeout: float = 10.0
  headers: dict[str, str] = field(default_factory=lambda: DEFAULT_HEADERS.copy())
  retries: int = 2
  enable_js: bool = False
  max_concurrency: int = 10
