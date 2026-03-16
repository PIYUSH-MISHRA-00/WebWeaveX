from __future__ import annotations

from webweavex.models import PageResult


class WebWeaveXPlugin:
  """Base plugin interface for WebWeaveX extensions."""

  name: str = "unnamed"

  def supports(self, url: str) -> bool:
    return False

  async def process(self, page: PageResult) -> None:
    return None
