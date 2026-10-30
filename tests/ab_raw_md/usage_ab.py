"""Fill token columns of the A/B test log from the session transcript (see AB.md).

Usage (from the repo root, after quitting the test session):
    python tests/ab_raw_md/usage_ab.py --session <session id or .jsonl path> [--slug sonnet-5-5]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("usage", HERE.parents[1] / "scripts/claude/4c_usage.py")
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)

usage.LOGS = HERE / "logs"  # also keeps sessions.csv lookups inside the test folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--slug", default="sonnet-5-5")
    args = parser.parse_args()
    sys.argv = [sys.argv[0], "--step", "step1", "--slug", args.slug, "--session", args.session]
    usage.main()
