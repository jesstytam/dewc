"""Run scripts/claude/4a_check.py with the A/B test paths (see AB.md).

Usage (from the repo root):
    python tests/ab_raw_md/check_ab.py <slug> [--paper <stem>]
"""

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check", HERE.parents[1] / "scripts/claude/4a_check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

check.ROOT = HERE
check.LOGS = HERE / "logs"
check.MD_OPT = HERE / "papers"  # Step 1 input (PAPERS) for this test

if __name__ == "__main__":
    check.main()
