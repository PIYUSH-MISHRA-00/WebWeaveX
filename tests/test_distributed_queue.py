import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "core"
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))
if str(CORE_DIR) not in sys.path:
  sys.path.insert(0, str(CORE_DIR))

from distributed.queue.redis_queue import RedisQueue


class FakeRedis:
  def __init__(self) -> None:
    self.storage: dict[str, list[str]] = {}

  def lpush(self, name: str, value: str) -> None:
    self.storage.setdefault(name, []).insert(0, value)

  def brpop(self, name: str, timeout: int = 0):
    values = self.storage.get(name, [])
    if not values:
      return None
    value = values.pop()
    return name, value


class DistributedQueueTests(unittest.TestCase):
  def test_enqueue_dequeue(self):
    client = FakeRedis()
    queue = RedisQueue(name="test", client=client)

    queue.enqueue("https://example.com/a")
    queue.enqueue("https://example.com/b")

    first = queue.dequeue(timeout=0)
    second = queue.dequeue(timeout=0)

    self.assertEqual(first, "https://example.com/a")
    self.assertEqual(second, "https://example.com/b")


if __name__ == "__main__":
  unittest.main()
