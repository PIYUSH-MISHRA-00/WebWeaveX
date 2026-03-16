# Plugins

WebWeaveX plugins allow you to extend extraction and post-processing for domain-specific
use cases without modifying core code.

## Plugin Structure

Each plugin lives under `plugins/<plugin-name>/plugin.py` and implements the
`WebWeaveXPlugin` interface.

```python
from webweavex.plugin_interface import WebWeaveXPlugin
from webweavex.models import PageResult

class MyPlugin(WebWeaveXPlugin):
  name = "my-plugin"

  def supports(self, url: str) -> bool:
    return "example.com" in url

  async def process(self, page: PageResult) -> None:
    page.metadata.meta["my_plugin"] = {"custom": "value"}
```

## Loading Behavior

The plugin loader scans the `plugins/` directory at runtime and registers any plugins
that implement `WebWeaveXPlugin`. Plugins are executed after core extraction finishes.

## Example

The repository ships with a YouTube plugin at `plugins/youtube/plugin.py`. It extracts
basic metadata such as title, description, channel, and video ID.
