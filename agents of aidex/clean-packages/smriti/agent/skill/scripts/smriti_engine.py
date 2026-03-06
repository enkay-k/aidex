#!/usr/bin/env python3
"""Skill wrapper for project Smriti utility."""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
runpy.run_path(str(ROOT / "utils" / "smriti_engine.py"), run_name="__main__")
