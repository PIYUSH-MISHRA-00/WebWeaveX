"""SSL certificate handling utilities."""

from __future__ import annotations

import ssl
from typing import Union

from .logging import get_logger

try:
  import certifi
except ImportError:  # pragma: no cover
  certifi = None

logger = get_logger(__name__)


def get_ssl_verify(config_ssl_verify: Union[bool, str]) -> Union[bool, str, ssl.SSLContext]:
  """
  Get SSL verification configuration for httpx.
  
  Args:
    config_ssl_verify: SSL verify setting from CrawlConfig
                      - True: use system certs or certifi
                      - False: disable verification
                      - str: path to CA bundle
  
  Returns:
    SSL verification setting suitable for httpx:
    - bool: True/False for default/disabled
    - str: path to CA bundle
    - ssl.SSLContext: custom SSL context
  """
  if isinstance(config_ssl_verify, str):
    # Path to CA bundle provided
    logger.info(f"Using custom CA bundle: {config_ssl_verify}")
    return config_ssl_verify
  
  if config_ssl_verify is False:
    # Explicitly disable verification
    logger.warning("SSL certificate verification DISABLED - use only for testing!")
    return False
  
  # Try to use system CA bundle (Windows, macOS, Linux)
  try:
    ctx = ssl.create_default_context()
    logger.info("SSL: Using system certificate store")
    return ctx
  except Exception as e:
    logger.warning(f"SSL: Failed to create system context: {e}")
    
    # Fallback to certifi
    if certifi is not None:
      ca_bundle = certifi.where()
      logger.info(f"SSL: Using certifi CA bundle: {ca_bundle}")
      return ca_bundle
    
    # Last resort: use httpx default
    logger.warning("SSL: No CA bundle found, using httpx defaults")
    return True
