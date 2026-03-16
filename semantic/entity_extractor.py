from __future__ import annotations

import re
from typing import Iterable

from webweavex.logging import get_logger

logger = get_logger(__name__)

try:
  import spacy
  from spacy.language import Language
except ImportError:  # pragma: no cover
  spacy = None
  Language = None

_SUPPORTED_LABELS = {"PERSON", "ORG", "GPE", "PRODUCT", "EVENT", "WORK_OF_ART"}

_KNOWN_ENTITIES: dict[str, str] = {
  "Guido van Rossum": "PERSON",
  "Python": "PRODUCT",
  "OpenAI": "ORG",
  "San Francisco": "GPE",
}

_NLP: Language | None = None


def _ensure_ruler(nlp: Language) -> None:
  if nlp.has_pipe("entity_ruler"):
    return
  ruler = nlp.add_pipe("entity_ruler", before="ner" if nlp.has_pipe("ner") else None)
  patterns = [{"label": label, "pattern": entity} for entity, label in _KNOWN_ENTITIES.items()]
  ruler.add_patterns(patterns)


def _load_model() -> Language | None:
  global _NLP
  if _NLP is not None:
    return _NLP

  if spacy is None:
    logger.warning("spaCy is not installed. Install with: pip install spacy")
    return None

  try:
    nlp = spacy.load("en_core_web_sm")
  except OSError:
    logger.warning(
      "spaCy model en_core_web_sm not found. Run: python -m spacy download en_core_web_sm"
    )
    nlp = spacy.blank("en")
  _ensure_ruler(nlp)
  _NLP = nlp
  return _NLP


def _fallback_entities(text: str) -> list[dict[str, str]]:
  results: list[dict[str, str]] = []
  for entity, label in _KNOWN_ENTITIES.items():
    if entity in text:
      results.append({"entity": entity, "type": label})
  return results


def extract_entities(text: str) -> list[dict[str, str]]:
  if not text:
    return []

  nlp = _load_model()
  if nlp is None:
    return _fallback_entities(text)

  doc = nlp(text)
  seen: set[tuple[str, str]] = set()
  entities: list[dict[str, str]] = []

  for ent in doc.ents:
    label = ent.label_
    if label not in _SUPPORTED_LABELS:
      continue
    value = ent.text.strip()
    if not value:
      continue
    key = (value, label)
    if key in seen:
      continue
    seen.add(key)
    entities.append({"entity": value, "type": label})

  if not entities:
    entities = _fallback_entities(text)

  return entities
