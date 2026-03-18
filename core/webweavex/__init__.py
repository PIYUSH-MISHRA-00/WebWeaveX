"""WebWeaveX core package."""

import os
import ssl
import sys
from pathlib import Path

# Ensure CA certificates are available for HTTPS requests.
# Some environments (including certain CI containers) may lack a default CA bundle.
try:
  import certifi
  cafile = ssl.get_default_verify_paths().cafile
  if not cafile or not os.path.exists(cafile):
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:  # pragma: no cover
  pass

ROOT = Path(__file__).resolve().parents[1]  # core
sys.path.insert(0, str(ROOT.parent))  # root

from .async_engine import AsyncWebWeaveX
from .config import CrawlConfig
from .engine import WebWeaveX
from .models import Link, Metadata, PageResult

__all__ = [
  "AsyncWebWeaveX",
  "CrawlConfig",
  "WebWeaveX",
  "Link",
  "Metadata",
  "PageResult",
]
