"""okflify — converts OKF bundles into HTML."""
from importlib.metadata import version, PackageNotFoundError

try:                       # single source of truth is pyproject.toml
    __version__ = version("okflify")
except PackageNotFoundError:   # running from a source tree, not installed
    __version__ = "0.0.0+source"

from .build import build  # noqa: F401,E402
