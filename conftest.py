"""Root conftest — ensures behave_model is importable when running from source."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so `import behave_model` works
# even without installing the package.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
