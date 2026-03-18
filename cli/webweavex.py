"""CLI wrapper for WebWeaveX.

This file exists to preserve the legacy entrypoint `python cli/webweavex.py`.
It ensures the installed `webweavex` package is imported instead of the local
script file which shares the same name.
"""

import sys
from pathlib import Path

# Ensure the repository root is prioritized so `import webweavex` resolves to the
# installed package (which lives in core/webweavex).
ROOT = Path(__file__).resolve().parents[1]
# Overwrite sys.path[0] (script directory) to avoid shadowing the package.
if len(sys.path) > 0:
    sys.path[0] = str(ROOT)
elif str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from webweavex.cli import main


if __name__ == "__main__":
    main()
