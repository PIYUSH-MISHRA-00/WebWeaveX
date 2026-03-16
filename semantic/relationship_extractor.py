from __future__ import annotations

import re

from webweavex.logging import get_logger

logger = get_logger(__name__)

_NAME = r"[A-Z][A-Za-z0-9._-]*(?:\s+[A-Z][A-Za-z0-9._-]*)*"

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
  ("created", re.compile(rf"(?P<source>{_NAME})\s+created\s+(?P<target>{_NAME})", re.IGNORECASE)),
  ("founded", re.compile(rf"(?P<source>{_NAME})\s+founded\s+(?P<target>{_NAME})", re.IGNORECASE)),
  ("works at", re.compile(rf"(?P<source>{_NAME})\s+works\s+at\s+(?P<target>{_NAME})", re.IGNORECASE)),
]


def extract_relationships(text: str) -> list[dict[str, str]]:
  if not text:
    return []

  relations: list[dict[str, str]] = []
  seen: set[tuple[str, str, str]] = set()

  for relation, pattern in _PATTERNS:
    for match in pattern.finditer(text):
      source = match.group("source").strip()
      target = match.group("target").strip()
      if not source or not target:
        continue
      key = (source, relation, target)
      if key in seen:
        continue
      seen.add(key)
      relations.append({"source": source, "relation": relation, "target": target})

  logger.info("Relationships detected %s", len(relations))
  return relations
