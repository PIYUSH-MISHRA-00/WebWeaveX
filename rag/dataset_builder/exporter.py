from __future__ import annotations

import csv
import json
from pathlib import Path


def export_jsonl(entries: list[dict[str, object]], path: str | Path) -> None:
  output_path = Path(path)
  with output_path.open("w", encoding="utf-8") as handle:
    for entry in entries:
      handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def export_csv(entries: list[dict[str, object]], path: str | Path) -> None:
  output_path = Path(path)
  if not entries:
    output_path.write_text("", encoding="utf-8")
    return

  fieldnames = list(entries[0].keys())
  with output_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(entries)


def export_markdown(entries: list[dict[str, object]], path: str | Path) -> None:
  output_path = Path(path)
  lines: list[str] = []
  for entry in entries:
    title = entry.get("title") or "Untitled"
    chunk_id = entry.get("chunk_id")
    lines.append(f"## {title} (Chunk {chunk_id})")
    lines.append(f"- URL: {entry.get('url')}")
    lines.append(f"- Source: {entry.get('source_domain')}")
    lines.append("")
    lines.append(str(entry.get("text", "")))
    lines.append("")

  output_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
