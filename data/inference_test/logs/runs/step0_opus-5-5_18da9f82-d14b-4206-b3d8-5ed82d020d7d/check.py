"""Check extraction output against the rules in CLAUDE.md.

Usage (from the repo root):
    python scripts/claude/check.py <slug> --paper <stem>   # after each paper in Step 1
    python scripts/claude/check.py <slug>                  # after all papers in Step 1
    python scripts/claude/check.py --step0                 # after Step 0

Only checks that need no reading of the paper; column rules are in references/metadata.csv. Never edits RESULT or LOG.
Writes a report to data/inference_test/logs/{slug}_check.csv (or md_opt_check.csv)
and exits 1 if any check fails.
"""

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "data/inference_test"  # test run only; never data/inference
MD_RAW = REPO / "data/papers_test/md"
MD_OPT = REPO / "data/papers_test/md_agents"
LOGS = ROOT / "logs"

TOKEN_COLS = ["n_requests", "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "total_tokens"]
LOG_HEADER = ["paper", "status", "n_rows", "started", "finished", "note"] + TOKEN_COLS
MD_LOG_HEADER = ["paper", "status", "pdf_pages", "n_tables", "n_fixes", "unresolved", "started", "finished", "note"] + TOKEN_COLS
STATUSES = {"done", "broken", "no_data"}

FIXED_YEARS = [
    "Age at first flower production from seed_repr3",
    "Time to first flower production resprout_repr3a",
    "Time to 50% flowering_repr4",
]
VARIABLE_UNIT = [
    "secondary_juvenile_period",
    "Time to 50% flowering",
    "Time to 80% flowering",
    "Recovery_time",
]
TIME_COLS = ["PJP mths", "primary_juvenile_period"] + FIXED_YEARS + VARIABLE_UNIT
DUP_KEY = ["scientific_name", "subsp", "Latitude", "Longitude", "Location_name",
           "Fire_type", "Fire_season_categorical", "File_name"]

TIME_RE = re.compile(r"[<>]?\d+(\.\d+)?(-\d+(\.\d+)?)?")
NUMBER_RE = re.compile(r"-?\d+(\.\d+)?")
SEASON_RE = re.compile(r"(Summer|Autumn|Winter|Spring)(; (Summer|Autumn|Winter|Spring))*")
PAGE_BREAK = "<!-- PAGE BREAK -->"
UTC_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
JUNK = {
    "page number prefix": re.compile(r"\{\d+\}<!-- PAGE BREAK -->"),
    "span tag": re.compile(r"<span id="),
    "br tag": re.compile(r"<br\s*/?>"),
}
DASH_RE = re.compile(r"[\u2013\u2014]")  # en dash, em dash
NAME_MARK_RE = re.compile(r"[?*]")
RANK_RE = re.compile(r"[a-z]+\. \S")  # subsp. / var. / f. / cv. ... + name
RANK_IN_SPECIES_RE = re.compile(r"(?:^|\s)(nothosubsp|subsp|ssp|nothovar|var|forma|f)\.?\s")
HYPHEN_SPACE_RE = re.compile(r"\s-|-\s")
CODE_SPACE_RE = re.compile(r"\s[?/;,)]|[?/;,(]\s")
APA_RE = re.compile(r"[^()]+ \(\d{4}[a-z]?\)\. .+")
NOTES_PAGE_RE = re.compile(r"\b(page|pg\.?|pp\.?)\s*\d", re.I)
LIGATURE_RE = re.compile(r"\b\w*(fi|fl) (re|res|rst|eld|elds|tted|ne|nal|nd|ve|gure|gures|ower|owers|owering|owered)\b")


def columns_from_claude_md():
    """Read the COLUMNS list from CLAUDE.md so both files share one definition."""
    text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    block = text[text.index("COLUMNS = ["):]
    block = block[:block.index("\n]")]
    return re.findall(r'^\s+\("([^"]+)", "', block, re.M)


class Report:
    def __init__(self):
        self.items = []

    def error(self, where, column, check, value=""):
        self.items.append(("error", where, column, check, value))

    def warn(self, where, column, check, value=""):
        self.items.append(("warning", where, column, check, value))

    def n(self, level):
        return sum(1 for item in self.items if item[0] == level)

    def write(self, path):
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["level", "where", "column", "check", "value"])
            w.writerows(self.items)


def read_csv(path, report, name):
    """Return rows as lists, or None if the file cannot be read."""
    if not path.exists():
        report.error(name, "", "file missing", str(path.relative_to(REPO)))
        return None
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        report.error(name, "", "not UTF-8", str(e))
        return None
    if "\r" in text:
        report.error(name, "", "CR line endings; use LF")
    return list(csv.reader(text.splitlines()))


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def papers_hash():
    """Same as: sha256sum data/papers_test/md_agents/*.md | LC_ALL=C sort | sha256sum (from the repo root)."""
    lines = sorted(f"{sha256_hex(p.read_bytes())}  {p.relative_to(REPO)}\n" for p in MD_OPT.glob("*.md"))
    return sha256_hex("".join(lines).encode("utf-8"))


def check_times(where, entry, report, need_finished=True):
    """started and finished must be UTC times from `date -u +%FT%TZ`, in order."""
    for col in ("started", "finished") if need_finished else ("started",):
        if not UTC_RE.fullmatch(entry.get(col, "")):
            report.error(where, col, "must be UTC time like 2026-10-02T08:04:26Z", entry.get(col, ""))
    if need_finished and UTC_RE.fullmatch(entry["started"]) and UTC_RE.fullmatch(entry["finished"]):
        if entry["finished"] < entry["started"]:
            report.error(where, "finished", "earlier than started", entry["finished"])


def check_tokens(where, entry, report):
    """Token cells: empty (agent) or whole numbers (filled by usage.py)."""
    for col in TOKEN_COLS:
        if entry.get(col, "") and not entry[col].isdigit():
            report.error(where, col, "empty or whole number; filled by usage.py", entry[col])


def decimals(value):
    return len(value.split(".")[1]) if "." in value else 0


def check_row(line, row, report):
    where = f"RESULT line {line}"
    for col, value in row.items():
        if value != value.strip():
            report.error(where, col, "leading or trailing space", value)
        if DASH_RE.search(value):
            report.error(where, col, "en or em dash; use ASCII hyphen '-'", value)
    for col in ("Source", "File_name"):
        if not row[col] or row[col] == "NA":
            report.error(where, col, "empty or NA")

    if row["Genus"] == "NA":  # NA row
        for col, value in row.items():
            if col not in ("Notes", "Source", "File_name") and value != "NA":
                report.error(where, col, "NA row: cell must be NA", value)
        if not row["Notes"] or row["Notes"] == "NA":
            report.error(where, "Notes", "NA row: reason missing")
        return

    for col, value in row.items():
        if value == "NA":
            report.error(where, col, "NA in data row; leave empty instead")
    for col in ("Genus", "Species"):
        if not row[col]:
            report.error(where, col, "empty")

    name = f"{row['Genus']} {row['Species']}"
    if row["scientific_name"] != name:
        report.error(where, "scientific_name", f"must be Genus + ' ' + Species: '{name}'", row["scientific_name"])
    for col in ("Genus", "Species", "subsp"):
        if NAME_MARK_RE.search(row[col]):
            report.error(where, col, "remove '?' or '*' from the name; printed form in Notes", row[col])
        if HYPHEN_SPACE_RE.search(row[col]):
            report.error(where, col, "space next to a hyphen; hyphenated epithet is one word ('novae- zelandiae' -> 'novae-zelandiae')", row[col])
    if row["Genus"] and not re.fullmatch(r"[A-Z][a-z]+", row["Genus"]):
        report.error(where, "Genus", "one capitalised word, no marks", row["Genus"])
    if RANK_IN_SPECIES_RE.search(row["Species"]):
        report.error(where, "Species", "rank word in Species; rank and name go in subsp", row["Species"])
    elif row["Species"] and not re.fullmatch(r"[a-z][a-z-]*", row["Species"]):
        report.warn(where, "Species", "not a plain lower-case epithet (fine for phrase names, e.g. 'sp. A')", row["Species"])
    if row["subsp"] and not RANK_RE.match(row["subsp"]):
        report.error(where, "subsp", "rank word + name, e.g. 'subsp. buxifolia', 'var. lanceolatus', 'f. glauca'", row["subsp"])
    if row["native_status"] and not re.fullmatch(r"[a-z]+( [a-z]+)*", row["native_status"]):
        report.error(where, "native_status", "paper's term in lower case, e.g. native, exotic", row["native_status"])
    if CODE_SPACE_RE.search(row["fire_response categorical_surv1"]):
        report.error(where, "fire_response categorical_surv1", "space next to '?', '/', ';', ',' or a bracket; remove it ('? r' -> '?r')", row["fire_response categorical_surv1"])
    family = row["Family"]
    if family and (family.isupper() or not re.match(r"[A-Z][a-z]", family)):
        report.warn(where, "Family", "only the first letter capitalised, e.g. Myrtaceae", family)
    if row["Source"] != row["File_name"] and not APA_RE.fullmatch(row["Source"]):
        report.warn(where, "Source", "does not look like APA: 'Author, A. B. (YYYY). Title. ...'", row["Source"])
    m = NOTES_PAGE_RE.search(row["Notes"])
    if m:
        report.warn(where, "Notes", "page reference: write 'p. N' (printed page) or 'PDF p. N'", m.group(0))

    lat, lon = row["Latitude"], row["Longitude"]
    for col, value, lo, hi in (("Latitude", lat, -44, -10), ("Longitude", lon, 112, 154)):
        if value:
            if not NUMBER_RE.fullmatch(value):
                report.error(where, col, "not a decimal number", value)
            elif not lo <= float(value) <= hi:
                report.error(where, col, f"outside {lo} to {hi}", value)

    for col in TIME_COLS:
        value = row[col]
        if value and not TIME_RE.fullmatch(value):
            report.error(where, col, "time format: number, min-max, or >/< bound", value)
    for col in FIXED_YEARS:
        value = row[col]
        if value and TIME_RE.fullmatch(value):
            if any(decimals(part) > 3 for part in value.lstrip("<>").split("-")):
                report.error(where, col, "more than 3 decimals", value)

    unit_needed = any(row[col] for col in VARIABLE_UNIT)
    if unit_needed and row["Time_unit"] not in ("days", "weeks", "months", "years"):
        report.error(where, "Time_unit", "must be days, weeks, months or years", row["Time_unit"])
    if not unit_needed and row["Time_unit"]:
        report.error(where, "Time_unit", "must be empty: no variable-unit time column filled", row["Time_unit"])

    pjp, repr4 = row["PJP mths"], row["Time to 50% flowering_repr4"]
    if pjp and repr4 and NUMBER_RE.fullmatch(pjp) and NUMBER_RE.fullmatch(repr4):
        if round(float(pjp) / 12, decimals(repr4)) != float(repr4):
            report.error(where, "Time to 50% flowering_repr4", f"should be PJP mths / 12 ({float(pjp) / 12:.3f})", repr4)

    season = row["Fire_season_categorical"]
    if season and not SEASON_RE.fullmatch(season):
        report.error(where, "Fire_season_categorical", "Summer|Autumn|Winter|Spring, joined by '; '", season)
    for col in ("Location_name", "resprouter_type"):
        if re.search(r"\s/\s", row[col]) or (col == "resprouter_type" and "/" in row[col]):
            report.warn(where, col, "several values: join with '; ' (keep '/' only if printed inside one value)", row[col])
    rain = row["Rainfall_mm"]
    if rain and not re.fullmatch(r"\d+(\.\d+)?(-\d+(\.\d+)?)?", rain):
        report.error(where, "Rainfall_mm", "not a number or min-max range", rain)


def check_step1(slug, paper, report):
    columns = columns_from_claude_md()
    result_path = ROOT / f"results/{slug}.csv"
    log_path = LOGS / f"{slug}_log.csv"
    result = read_csv(result_path, report, "RESULT")
    log = read_csv(log_path, report, "LOG")
    if result is None or log is None:
        return

    # file level
    if not result or result[0] != columns:
        report.error("RESULT line 1", "", f"header must be the {len(columns)} COLUMNS names in order")
        return
    if not log or log[0] != LOG_HEADER:
        report.error("LOG line 1", "", "header must be " + ",".join(LOG_HEADER))
        return
    rows = []
    for line, cells in enumerate(result[1:], 2):
        if len(cells) != len(columns):
            report.error(f"RESULT line {line}", "", f"{len(cells)} cells, expected {len(columns)}")
        else:
            rows.append((line, dict(zip(columns, cells))))

    log_rows = [dict(zip(LOG_HEADER, cells)) for cells in log[1:] if len(cells) == len(LOG_HEADER)]
    if len(log_rows) != len(log) - 1:
        report.error("LOG", "", f"every line needs {len(LOG_HEADER)} cells")
    runs = [r for r in log_rows if r["paper"] == "_run"]
    papers = [r for r in log_rows if r["paper"] != "_run"]
    if not runs:
        report.error("LOG", "paper", "no _run line")
    if runs:  # the current run must hash the files it used
        expected = {"claude_md_sha256": sha256_hex((REPO / "CLAUDE.md").read_bytes()), "papers_sha256": papers_hash()}
        for field, value in expected.items():
            m = re.search(field + r"=([0-9a-f]{64})", runs[-1]["note"])
            if m and m.group(1) != value:
                report.error("LOG _run", "note", f"{field} does not match the current files; recompute with the command in CLAUDE.md", m.group(1))
    for r in runs:
        check_times("LOG _run", r, report, need_finished=False)
        for field in ("model=", "date=", "git=", "claude_md_sha256="):
            if field not in r["note"]:
                report.error("LOG _run", "note", f"missing {field}", r["note"])

    # which papers to check
    if paper:
        papers = [r for r in papers if r["paper"] == paper]
        if not papers:
            report.error("LOG", "paper", "paper not in LOG; write its LOG line before checking", paper)
            return
    else:
        expected = sorted(p.stem for p in MD_OPT.glob("*.md"))
        counts = Counter(r["paper"] for r in papers)
        for stem in expected:
            if counts[stem] != 1:
                report.error("LOG", "paper", f"{counts[stem]} LOG lines, expected 1", stem)
        for stem in counts:
            if stem not in expected:
                report.error("LOG", "paper", "not a file in PAPERS", stem)

    stems = {r["paper"] for r in log_rows if r["paper"] != "_run"}
    for line, row in rows:
        if row["File_name"] not in stems:
            report.error(f"RESULT line {line}", "File_name", "matches no LOG paper", row["File_name"])

    # paper level
    checked_stems = set()
    for r in papers:
        where = f"LOG {r['paper']}"
        if r["status"] not in STATUSES:
            report.error(where, "status", "must be done, broken or no_data", r["status"])
        check_times(where, r, report)
        check_tokens(where, r, report)
        checked_stems.add(r["paper"])
        paper_rows = [(line, row) for line, row in rows if row["File_name"] == r["paper"]]
        if not paper_rows:
            report.error(where, "", "no rows in RESULT")
        if str(len(paper_rows)) != r["n_rows"]:
            report.error(where, "n_rows", f"RESULT has {len(paper_rows)} rows", r["n_rows"])
        if r["status"] in ("broken", "no_data") and not any(row["Genus"] == "NA" for _, row in paper_rows):
            report.error(where, "status", f"{r['status']} paper needs an NA row")
        citations = {row["Source"] for _, row in paper_rows}
        if len(citations) > 1:
            report.error(where, "Source", f"{len(citations)} different Source strings; use one", " | ".join(sorted(citations)))

    # row level, then duplicates
    checked = [(line, row) for line, row in rows if paper is None or row["File_name"] in checked_stems]
    for line, row in checked:
        check_row(line, row, report)
    # Location_name with coordinates: only when several sites of the paper share those coordinates
    names = {}
    checked_sites = [(line, row) for line, row in checked if row["Genus"] != "NA"]  # NA rows are checked in check_row
    for _, row in checked_sites:
        if row["Latitude"] or row["Longitude"]:
            names.setdefault((row["File_name"], row["Latitude"], row["Longitude"]), set()).add(row["Location_name"])
    for line, row in checked_sites:
        if row["Location_name"] and (row["Latitude"] or row["Longitude"]):
            if len(names[(row["File_name"], row["Latitude"], row["Longitude"])] - {""}) < 2:
                report.error(f"RESULT line {line}", "Location_name", "fill only when coordinates are empty or shared by several named sites", row["Location_name"])
    seen = {}
    for line, row in checked:
        if row["Genus"] == "NA":
            continue
        key = tuple(row[c] for c in DUP_KEY)
        if key in seen:
            first_line, first_row = seen[key]
            message = f"duplicate of line {first_line} on {', '.join(DUP_KEY)}"
            if all(r["Notes"].startswith("separate entry in paper") for r in (row, first_row)):
                report.warn(f"RESULT line {line}", "", message + " (marked separate entry in paper)")
            else:
                report.error(f"RESULT line {line}", "", message)
        else:
            seen[key] = (line, row)


def check_step0(report):
    log = read_csv(LOGS / "md_opt_log.csv", report, "MD_LOG")
    if log is None:
        return
    if not log or log[0] != MD_LOG_HEADER:
        report.error("MD_LOG line 1", "", "header must be " + ",".join(MD_LOG_HEADER))
        return
    log_rows = [dict(zip(MD_LOG_HEADER, cells)) for cells in log[1:]]
    counts = Counter(r["paper"] for r in log_rows)

    for md in sorted(MD_RAW.glob("*.md")):
        stem, where = md.stem, f"MD_OPT {md.stem}"
        if counts[stem] != 1:
            report.error("MD_LOG", "paper", f"{counts[stem]} lines, expected 1", stem)
        out = MD_OPT / f"{stem}.md"
        if not out.exists():
            report.error(where, "", "file missing")
            continue
        text = out.read_text(encoding="utf-8")
        if not text.rstrip().splitlines()[-1].startswith("<!-- md_opt:"):
            report.error(where, "", "no <!-- md_opt: end comment")
        entry = next((r for r in log_rows if r["paper"] == stem), None)
        if entry:
            check_times(f"MD_LOG {stem}", entry, report)
            check_tokens(f"MD_LOG {stem}", entry, report)
        if entry and entry["status"] == "done":
            breaks = text.count(PAGE_BREAK)
            if not entry["pdf_pages"].isdigit():
                report.error("MD_LOG", "pdf_pages", "not a whole number", entry["pdf_pages"])
            elif breaks + 1 != int(entry["pdf_pages"]):
                report.error(where, "", f"{breaks} page breaks, expected {int(entry['pdf_pages']) - 1}")
        for name, pattern in JUNK.items():
            n = len(pattern.findall(text))
            if n:
                report.error(where, "", f"{name} left: {n}")
        for m in LIGATURE_RE.finditer(text):
            report.warn(where, "", "possible split ligature", m.group(0))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", nargs="?", help="agent slug, e.g. opus-5-5")
    parser.add_argument("--paper", help="file stem of one paper; check only its rows")
    parser.add_argument("--step0", action="store_true", help="check Step 0 output instead")
    args = parser.parse_args()
    if not args.step0 and not args.slug:
        parser.error("give a slug, or --step0")

    report = Report()
    if args.step0:
        check_step0(report)
        out = LOGS / "md_opt_check.csv"
        scope = "Step 0"
    else:
        check_step1(args.slug, args.paper, report)
        out = LOGS / f"{args.slug}_check.csv"
        scope = f"{args.slug}" + (f" | paper {args.paper}" if args.paper else " | all papers")

    report.write(out)
    print(f"check {scope} | errors {report.n('error')} | warnings {report.n('warning')} | report {out.relative_to(REPO)}")
    for level, where, column, check, value in report.items[:20]:
        print(f"    {level}: {where} | {column} | {check} | {value}")
    if len(report.items) > 20:
        print(f"    ... {len(report.items) - 20} more in report")
    sys.exit(1 if report.n("error") else 0)


if __name__ == "__main__":
    main()
