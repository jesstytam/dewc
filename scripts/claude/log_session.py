"""Log a finished pipeline session (Step 0 or Step 1).

Runs as a SessionEnd hook (reads the hook JSON from stdin), or by hand:
    python scripts/claude/log_session.py --session <session id or .jsonl path>

Does nothing for sessions whose prompts never ask to "Run Step 0" or "Run Step 1".
For a pipeline session it:
  1. copies the session transcript to logs/runs/{step}_{slug}_{session}/transcript.jsonl;
  2. snapshots the rules (CLAUDE.md, check.py, template.csv, metadata.csv) and the step's outputs into the same folder (Step 0: md_opt_log.csv and
     md_opt_check.csv; Step 1: results/{slug}.csv, {slug}_log.csv, {slug}_check.csv);
  3. adds the session's line to logs/sessions.csv (once per session);
  4. fills the token columns in the step's log and in sessions.csv (usage.py).
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage  # noqa: E402

REPO = usage.REPO
ROOT = REPO / "data/inference_test"  # test run only; never data/inference
LOGS = ROOT / "logs"
AGENTS = {"claude-opus-5-5": "opus-5-5", "claude-sonnet-5-5": "sonnet-5-5"}
SESSIONS_HEADER = ["date", "step", "slug", "models", "claude_version", "session_id"]
STEP_RE = re.compile(r"\s*Run Step ([01])\b")


def user_texts(entries):
    for e in entries:
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        content = (e.get("message") or {}).get("content")
        if isinstance(content, str):
            yield content
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    yield c["text"]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--session", help="session id or .jsonl path; default: read SessionEnd hook JSON from stdin")
    args = parser.parse_args()
    if args.session:
        path, _ = usage.transcript_files(args.session)
    else:
        hook = json.load(sys.stdin)
        path = Path(hook["transcript_path"])
    if not path.exists():
        return
    session = path.stem
    entries = [json.loads(line) for line in open(path, encoding="utf-8")]

    prompt = next((t for t in user_texts(entries) if STEP_RE.match(t)), None)
    if prompt is None:
        return  # not a pipeline session
    step = "step0" if STEP_RE.match(prompt).group(1) == "0" else "step1"
    if step == "step1" and "Process only" in prompt:
        step = "step1-trial"
    models = sorted({(e.get("message") or {}).get("model") for e in entries if e.get("type") == "assistant"} - {None, "<synthetic>"})
    slugs = {AGENTS.get(m, "unknown") for m in models}
    slug = slugs.pop() if len(slugs) == 1 else "mixed"
    times = [e["timestamp"] for e in entries if e.get("timestamp")]
    start = usage.parse_time(times[0]).astimezone()
    version = next((e["version"] for e in entries if e.get("version")), "")

    # 1-2. transcript and output snapshot
    run_dir = LOGS / "runs" / f"{step}_{slug}_{session}"
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, run_dir / "transcript.jsonl")
    for f in (REPO / "CLAUDE.md", REPO / "scripts/claude/check.py", ROOT / "references/template.csv", ROOT / "references/metadata.csv"):
        if not (run_dir / f.name).exists():  # first logging of the session = closest to the run
            shutil.copy2(f, run_dir / f.name)

    # 3. sessions.csv line
    sessions = LOGS / "sessions.csv"
    if not sessions.exists():
        with open(sessions, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerow(SESSIONS_HEADER + usage.USAGE_COLS)
    if not any(r["session_id"] == session for r in csv.DictReader(open(sessions, encoding="utf-8", newline=""))):
        header = next(csv.reader(open(sessions, encoding="utf-8", newline="")))
        row = dict(zip(SESSIONS_HEADER, [start.strftime("%Y-%m-%d_%H%M"), step, slug, "|".join(models), version, session]))
        with open(sessions, "a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=header, restval="", lineterminator="\n").writerow(row)

    # 4. token columns (only for a known agent, whose log the step wrote)
    if slug in AGENTS.values():
        subprocess.run([sys.executable, str(Path(usage.__file__)), "--step", "step0" if step == "step0" else "step1",
                        "--slug", slug, "--session", str(path)], check=False)

    outputs = ([LOGS / "md_opt_log.csv", LOGS / "md_opt_check.csv"] if step == "step0" else
               [ROOT / f"results/{slug}.csv", LOGS / f"{slug}_log.csv", LOGS / f"{slug}_check.csv"])
    for f in outputs:
        if f.exists():
            shutil.copy2(f, run_dir / f.name)
    print(f"logged {step} | {slug} | session {session} | {run_dir.relative_to(REPO)}", file=sys.stderr)


if __name__ == "__main__":
    main()
