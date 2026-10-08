"""Run scripts/claude/check.py with the A/B test paths (see AB.md).

Usage (from the repo root):
    python tests/ab_raw_md/check_ab.py <slug> [--paper <stem>]
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts/claude"))
import check  # noqa: E402

check.ROOT = HERE
check.LOGS = HERE / "logs"
check.MD_OPT = HERE / "papers"  # Step 1 input (PAPERS) for this test

if __name__ == "__main__":
    check.main()
