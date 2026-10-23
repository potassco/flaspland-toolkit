"""
Allow running flaspland with `python -m flaspland`.
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
