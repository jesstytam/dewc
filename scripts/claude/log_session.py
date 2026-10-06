"""Log a finished pipeline session (Step 0 or Step 1).

Runs as a SessionEnd hook (reads the hook JSON from stdin), or by hand:
    python scripts/claude/log_session.py --session <session id or .jsonl path>

Does nothing for sessions whose prompts never ask to "Run Step 0" or "Run Step 1".
A session can run several steps (e.g. "Run Step 0", then "Run Step 1"). Each step's part of
the session runs from its prompt to the next prompt for a different step (or the session end).
For each step in a pipeline session it:
  1. copies the session transcript to logs/runs/{step}_{slug}_{session}/transcript.jsonl;
  2. snapshots the rules (CLAUDE.md, check.py, template.csv, metadata.csv) and the step's outputs into the same folder (Step 0: md_opt_log.csv and
     md_opt_check.csv; Step 1: results/{slug}.csv, {slug}_log.csv, {slug}_check.csv);
  3. adds the step's line to logs/sessions.csv (once per session and step);
  4. fills the token columns in the step's log and in sessions.csv, counting only the step's part of the session (usage.py --window).
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
    """(entry, text) for each user prompt."""
    for e in entries:
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        content = (e.get("message") or {}).get("content")
        if isinstance(content, str):
            yield e, content
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    yield e, c["text"]


def step_of(prompt):
    step = "step0" if STEP_RE.match(prompt).group(1) == "0" else "step1"
    if step == "step1" and "Process only" in prompt:
        step = "step1-trial"
    return step


def segments(entries):
    """[(step, start, end)] in session order; consecutive prompts for the same step are merged; end None = session end."""
    result = []
    for e, text in user_texts(entries):
        if not STEP_RE.match(text):
            continue
        step = step_of(text)
        if result and result[-1][0] == step:
            continue
        if any(r[0] == step for r in result):
            print(f"warning: {step} prompted again after another step; logging only its first part", file=sys.stderr)
            continue
        if result:
            result[-1][2] = e["timestamp"]
        result.append([step, e["timestamp"], None])
    return [tuple(r) for r in result]


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

    steps = segments(entries)
    if not steps:
        return  # not a pipeline session
    models = sorted({(e.get("message") or {}).get("model") for e in entries if e.get("type") == "assistant"} - {None, "<synthetic>"})
    slugs = {AGENTS.get(m, "unknown") for m in models}
    slug = slugs.pop() if len(slugs) == 1 else "mixed"
    version = next((e["version"] for e in entries if e.get("version")), "")
    for step, since, until in steps:
        log_step(path, session, step, since, until, slug, models, version)


def log_step(path, session, step, since, until, slug, models, version):
    start = usage.parse_time(since).astimezone()

    # 1-2. transcript and output snapshot
    run_dir = LOGS / "runs" / f"{step}_{slug}_{session}"
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, run_dir / "transcript.jsonl")
    for f in (REPO / "CLAUDE.md", REPO / "scripts/claude/check.py", ROOT / "references/template.csv", ROOT / "references/metadata.csv"):
        if not (run_dir / f.name).exists():  # first logging of the session = closest to the run
            shutil.copy2(f, run_dir / f.name)

    # 3. sessions.csv line, one per session and step
    sessions = LOGS / "sessions.csv"
    if not sessions.exists():
        with open(sessions, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerow(SESSIONS_HEADER + usage.USAGE_COLS)
    if not any((r["session_id"], r["step"]) == (session, step) for r in csv.DictReader(open(sessions, encoding="utf-8", newline=""))):
        header = next(csv.reader(open(sessions, encoding="utf-8", newline="")))
        row = dict(zip(SESSIONS_HEADER, [start.strftime("%Y-%m-%d_%H%M"), step, slug, "|".join(models), version, session]))
        with open(sessions, "a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=header, restval="", lineterminator="\n").writerow(row)

    # 4. token columns (only for a known agent, whose log the step wrote), counting only this step's part of the session
    if slug in AGENTS.values():
        subprocess.run([sys.executable, str(Path(usage.__file__)), "--step", step, "--slug", slug,
                        "--session", str(path), "--window", f"{since},{until or ''}"], check=False)

    outputs = ([LOGS / "md_opt_log.csv", LOGS / "md_opt_check.csv"] if step == "step0" else
               [ROOT / f"results/{slug}.csv", LOGS / f"{slug}_log.csv", LOGS / f"{slug}_check.csv"])
    for f in outputs:
        if f.exists():
            shutil.copy2(f, run_dir / f.name)
    print(f"logged {step} | {slug} | session {session} | {run_dir.relative_to(REPO)}", file=sys.stderr)


if __name__ == "__main__":
    main()
