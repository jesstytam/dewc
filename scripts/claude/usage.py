"""Token usage per paper for one Claude Code session.

Usage (from the repo root, after quitting the session):
    python scripts/claude/usage.py --step step0 --slug opus-5-5 --session <session id or .jsonl path>
    python scripts/claude/usage.py --step step1 --slug sonnet-5-5 --session <...>

Reads the session transcript (~/.claude/projects/<project>/<session>.jsonl, plus any
subagent transcripts in <session>/subagents/) and the step's log. Each API response is
assigned to the paper whose started-finished window in the log contains its timestamp;
responses outside every window (setup, final checks, wrap-up) go to "_other".

Fills the token columns (USAGE_COLS) of each paper's line in the step's log, and of the
session's line in logs/sessions.csv (whole-session totals, including _other). Adds the
columns to a file's header if missing. Changes no other cells.
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOGS = REPO / "data/inference_test/logs"  # test run only; never data/inference
TRANSCRIPTS = Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(REPO))
TOKENS = ["input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"]
USAGE_COLS = ["n_requests"] + TOKENS + ["total_tokens"]


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def transcript_files(session):
    path = Path(session)
    if path.suffix != ".jsonl":
        path = TRANSCRIPTS / f"{session}.jsonl"
    if not path.exists():
        sys.exit(f"transcript not found: {path}")
    subagents = sorted((path.parent / path.stem / "subagents").glob("*.jsonl"))
    return path, [path] + subagents


def responses(files):
    """One record per API response; a response split over several entries is counted once."""
    seen = {}
    for f in files:
        for line in open(f, encoding="utf-8"):
            entry = json.loads(line)
            message = entry.get("message") or {}
            if entry.get("type") != "assistant" or "usage" not in message:
                continue
            key = message.get("id") or entry.get("requestId") or entry.get("uuid")
            if key not in seen:
                seen[key] = {
                    "time": parse_time(entry["timestamp"]),
                    "model": message.get("model", ""),
                    **{t: message["usage"].get(t) or 0 for t in TOKENS},
                }
    return sorted(seen.values(), key=lambda r: r["time"])


def log_path(step, slug):
    return LOGS / ("md_opt_log.csv" if step == "step0" else f"{slug}_log.csv")


def fill(path, key, values):
    """Write USAGE_COLS values into the rows of a CSV whose `key` column matches."""
    rows = list(csv.DictReader(open(path, encoding="utf-8", newline="")))
    header = next(csv.reader(open(path, encoding="utf-8", newline="")))
    header += [c for c in USAGE_COLS if c not in header]
    for row in rows:
        if row[key] in values:
            row.update({c: values[row[key]][c] for c in USAGE_COLS})
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, restval="", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def windows(step, slug):
    log = log_path(step, slug)
    if not log.exists():
        sys.exit(f"log not found: {log}")
    result = []
    for row in csv.DictReader(open(log, encoding="utf-8", newline="")):
        if row["paper"] == "_run":
            continue
        if not row.get("started") or not row.get("finished"):
            print(f"    warning: {row['paper']} has no started/finished times; its tokens go to _other")
            continue
        result.append((row["paper"], parse_time(row["started"]), parse_time(row["finished"])))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--step", required=True, help="step0, step1-trial or step1")
    parser.add_argument("--slug", required=True, help="agent slug, e.g. opus-5-5")
    parser.add_argument("--session", required=True, help="session id or path to its .jsonl transcript")
    args = parser.parse_args()

    main_file, files = transcript_files(args.session)
    papers = windows(args.step, args.slug)
    totals = {}
    for r in responses(files):
        paper = next((p for p, start, end in papers if start <= r["time"] <= end), "_other")
        row = totals.setdefault(paper, {"n_requests": 0, "models": set(), **{t: 0 for t in TOKENS}})
        row["n_requests"] += 1
        row["models"].add(r["model"])
        for t in TOKENS:
            row[t] += r[t]

    for row in totals.values():
        row["total_tokens"] = sum(row[t] for t in TOKENS)
    grand = {c: sum(row[c] for row in totals.values()) for c in USAGE_COLS}
    grand["models"] = set().union(*(row["models"] for row in totals.values()))

    fill(log_path(args.step, args.slug), "paper", {p: totals[p] for p, _, _ in papers if p in totals})
    sessions = LOGS / "sessions.csv"
    if sessions.exists() and any(r["session_id"] == main_file.stem for r in csv.DictReader(open(sessions, encoding="utf-8", newline=""))):
        fill(sessions, "session_id", {main_file.stem: grand})
    else:
        print(f"    warning: session {main_file.stem} not in {sessions.relative_to(REPO)}; session totals not written")

    print(f"usage {args.step} | {args.slug} | session {main_file.stem} | models {'|'.join(sorted(grand['models']))}")
    order = [p for p, _, _ in papers if p in totals] + (["_other"] if "_other" in totals else [])
    for paper in order + ["_total"]:
        row = grand if paper == "_total" else totals[paper]
        print(f"    {paper[:45]:45} requests {row['n_requests']:5} | output {row['output_tokens']:>9,} | total {row['total_tokens']:>12,}")
    print(f"    written to {log_path(args.step, args.slug).relative_to(REPO)} (per paper) and {sessions.relative_to(REPO)} (session total)")

if __name__ == "__main__":
    main()
