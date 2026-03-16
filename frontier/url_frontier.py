from __future__ import annotations

import heapq


class URLFrontier:
  """Priority queue and deduplication for URLs with depth control."""

  def __init__(self, max_depth: int = 3) -> None:
    self._heap: list[tuple[float, int, str, int]] = []
    self._visited: set[str] = set()
    self._max_depth = max_depth
    self._counter = 0

  def add(self, url: str, depth: int = 0, priority: float = 0.0) -> None:
    if depth > self._max_depth:
      return
    if url in self._visited:
      return
    self._visited.add(url)
    # Use negative priority for max-heap behavior.
    heapq.heappush(self._heap, (-priority, self._counter, url, depth))
    self._counter += 1

  def add_many(self, urls: list[str], depth: int = 0, priority: float = 0.0) -> None:
    for url in urls:
      self.add(url, depth=depth, priority=priority)

  def next(self) -> tuple[str, int] | None:
    if not self._heap:
      return None
    _, _, url, depth = heapq.heappop(self._heap)
    return url, depth

  def size(self) -> int:
    return len(self._heap)

  def visited_count(self) -> int:
    return len(self._visited)
