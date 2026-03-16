from __future__ import annotations

from urllib.parse import urljoin, urlparse, urlunparse


def normalize_url(url: str) -> str:
  parsed = urlparse(url)
  if not parsed.scheme:
    return url
  scheme = parsed.scheme.lower()
  netloc = parsed.netloc.lower()
  path = parsed.path or "/"
  normalized = parsed._replace(scheme=scheme, netloc=netloc, path=path, fragment="")
  return urlunparse(normalized)


def resolve_relative(base: str, link: str) -> str:
  return urljoin(base, link)


def deduplicate_urls(urls: list[str]) -> list[str]:
  seen: set[str] = set()
  result: list[str] = []
  for url in urls:
    normalized = normalize_url(url)
    if normalized in seen:
      continue
    seen.add(normalized)
    result.append(normalized)
  return result
