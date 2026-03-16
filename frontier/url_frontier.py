from __future__ import annotations

from collections import deque


class URLFrontier:
  """Queue and deduplication for URLs with depth control."""

  def __init__(self, max_depth: int = 3) -> None:
    self._queue: deque[tuple[str, int]] = deque()
    self._visited: set[str] = set()
    self._max_depth = max_depth

  def add(self, url: str, depth: int = 0) -> None:
    if depth > self._max_depth:
      return
    if url in self._visited:
      return
    self._visited.add(url)
    self._queue.append((url, depth))

  def add_many(self, urls: list[str], depth: int = 0) -> None:
    for url in urls:
      self.add(url, depth)

  def next(self) -> tuple[str, int] | None:
    if not self._queue:
      return None
    return self._queue.popleft()

  def size(self) -> int:
    return len(self._queue)

  def visited_count(self) -> int:
    return len(self._visited)
