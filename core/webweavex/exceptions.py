class WebWeaveXError(Exception):
  """Base exception for WebWeaveX core."""


class FetchError(WebWeaveXError):
  """Raised when an HTTP fetch fails after retries."""


class ParseError(WebWeaveXError):
  """Raised when HTML parsing fails unexpectedly."""
