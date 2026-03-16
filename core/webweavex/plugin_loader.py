from __future__ import annotations

import importlib.util
import inspect
import os
from pathlib import Path

from .logging import get_logger
from .plugin_interface import WebWeaveXPlugin

logger = get_logger(__name__)

_PLUGIN_REGISTRY: list[WebWeaveXPlugin] = []
_LOADED = False


def _default_plugins_dir() -> Path:
  env_path = os.getenv("WEBWEAVEX_PLUGINS_DIR")
  if env_path:
    return Path(env_path)
  return Path(__file__).resolve().parents[2] / "plugins"


def _load_module(module_name: str, path: Path):
  spec = importlib.util.spec_from_file_location(module_name, path)
  if spec is None or spec.loader is None:
    raise ImportError(f"Unable to load plugin module {module_name}")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def _collect_plugins(module) -> list[WebWeaveXPlugin]:
  instances: list[WebWeaveXPlugin] = []
  for _, obj in inspect.getmembers(module):
    if isinstance(obj, WebWeaveXPlugin):
      instances.append(obj)
      continue
    if inspect.isclass(obj) and issubclass(obj, WebWeaveXPlugin) and obj is not WebWeaveXPlugin:
      try:
        instances.append(obj())
      except Exception:
        logger.exception("Failed to instantiate plugin %s", obj)
  return instances


def load_plugins(plugins_dir: Path | None = None) -> list[WebWeaveXPlugin]:
  global _LOADED
  if _LOADED:
    return list(_PLUGIN_REGISTRY)

  _LOADED = True
  plugins_path = Path(plugins_dir) if plugins_dir else _default_plugins_dir()
  if not plugins_path.exists():
    logger.info("No plugins directory found at %s", plugins_path)
    return list(_PLUGIN_REGISTRY)

  for plugin_dir in sorted(plugins_path.iterdir()):
    if not plugin_dir.is_dir():
      continue
    plugin_file = plugin_dir / "plugin.py"
    if not plugin_file.exists():
      continue
    module_name = f"webweavex_plugins.{plugin_dir.name}"
    try:
      module = _load_module(module_name, plugin_file)
    except Exception:
      logger.exception("Failed to load plugin module at %s", plugin_file)
      continue

    for plugin in _collect_plugins(module):
      _PLUGIN_REGISTRY.append(plugin)
      plugin_name = getattr(plugin, "name", plugin.__class__.__name__)
      logger.info("Plugin loaded %s", plugin_name)

  return list(_PLUGIN_REGISTRY)


def get_plugins() -> list[WebWeaveXPlugin]:
  if not _LOADED:
    load_plugins()
  return list(_PLUGIN_REGISTRY)
