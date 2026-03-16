from __future__ import annotations

import asyncio
from urllib import robotparser
from urllib.parse import urlparse

import httpx

from .config import CrawlConfig
from .logging import get_logger

logger = get_logger(__name__)


class RobotsHandler:
  """Robots.txt handler with per-domain caching."""

  def __init__(self, config: CrawlConfig, client: httpx.AsyncClient | None = None) -> None:
    self._config = config
    self._client = client or httpx.AsyncClient(
      timeout=config.timeout,
      headers=config.headers,
      follow_redirects=True,
    )
    self._owns_client = client is None
    self._cache: dict[str, robotparser.RobotFileParser] = {}
    self._lock = asyncio.Lock()

  async def allowed(self, url: str) -> bool:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
      return True
    base = f"{parsed.scheme}://{parsed.netloc}"
    parser = await self._get_parser(base)
    user_agent = self._user_agent()
    allowed = parser.can_fetch(user_agent, url)
    if not allowed:
      logger.info("Robots blocked %s", url)
    return allowed

  async def _get_parser(self, base: str) -> robotparser.RobotFileParser:
    async with self._lock:
      if base in self._cache:
        return self._cache[base]

      robots_url = f"{base}/robots.txt"
      parser = robotparser.RobotFileParser()
      parser.set_url(robots_url)

      try:
        response = await self._client.get(robots_url)
        if response.status_code >= 400:
          parser.parse([])
        else:
          parser.parse(response.text.splitlines())
      except httpx.HTTPError:
        parser.parse([])

      self._cache[base] = parser
      return parser

  def _user_agent(self) -> str:
    headers = self._config.headers
    return headers.get("User-Agent") or headers.get("user-agent") or "*"

  async def close(self) -> None:
    if self._owns_client:
      await self._client.aclose()
