#!/usr/bin/env python3
"""Backward-compatible entry point for the source checkout."""

from pathlib import Path
import sys


SOURCE_DIR = Path(__file__).resolve().parent / "src"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from lcr.cli import main


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if not arguments or arguments[0].startswith("-"):
        arguments = ["review", *arguments]
    raise SystemExit(main(arguments))
