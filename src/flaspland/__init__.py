"""
Generate Flatland railway environments and solve them with answer set programming.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("flaspland")
except PackageNotFoundError:  # running from a source tree without installing
    __version__ = "unknown"
