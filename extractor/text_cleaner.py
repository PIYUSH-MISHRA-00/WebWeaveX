from __future__ import annotations

import re

_NAV_TOKENS = {
  "home",
  "about",
  "contact",
  "pricing",
  "login",
  "sign in",
  "sign up",
  "signup",
  "privacy",
  "terms",
  "support",
}


def clean_text(text: str) -> str:
  if not text:
    return ""

  cleaned_lines: list[str] = []
  for raw_line in text.splitlines():
    line = re.sub(r"\s+", " ", raw_line).strip()
    if not line:
      continue
    if line.lower() in _NAV_TOKENS:
      continue
    cleaned_lines.append(line)

  return "\n".join(cleaned_lines)
