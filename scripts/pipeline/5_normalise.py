"""Normalise raw Step 1 extraction into the final results.

Usage (from the repo root, after Step 1):
    python scripts/pipeline/5_normalise.py opus-5-5 sonnet-5-5
    python scripts/claude/check.py opus-5-5 --final        # then check the output

Reads data/inference_test/results/{slug}_raw.csv (values as printed in the papers) and writes
data/inference_test/results/{slug}.csv. Never edits the raw file. All unit conversion and
formatting happens here, not in the agents:
- time cells '<value> <unit>' are converted to each column's unit (rules below)
- primary juvenile period in months -> pjp_mths, and time_to_50_percent_flowering_repr4 = months / 12
- variable-unit columns keep the paper's unit and get time_unit (VARIABLE_UNIT_TARGET changes this)
- error_value is converted with its time column
- every conversion adds '<column> converted from <value> <unit>' at the start of notes
- case, dashes and range spacing follow CLAUDE.md; scientific_name and pdf_path are filled
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "data/inference_test/results"  # test run only; never data/inference
PDF_CLEAN = "data/papers_test/pdf_clean/"

#column units of the final dataset
YEARS_COLS = [
    "age_at_first_flower_production_from_seed_repr3",
    "time_to_first_flower_production_resprout_repr3a",
    "time_to_50_percent_flowering_repr4",
]
VARIABLE_COLS = [
    "secondary_juvenile_period",
    "time_to_50_percent_flowering",
    "time_to_80_percent_flowering",
    "recovery_time",
]
PJP = "primary_juvenile_period"
VARIABLE_UNIT_TARGET = None  # None: keep the paper's unit (mixed row: most common unit); or "years", "months", ...
FILLED_HERE = ["pjp_mths", "time_unit", "scientific_name", "pdf_path"]  # agents leave these empty in raw

#conversion factors from CLAUDE.md: years = months / 12 = weeks / 52 = days / 365; months = weeks / 4.33 = days / 30.4
FACTOR = {
    "years": {"years": 1, "months": 1 / 12, "weeks": 1 / 52, "days": 1 / 365},
    "months": {"years": 12, "months": 1, "weeks": 1 / 4.33, "days": 1 / 30.4},
    "weeks": {"years": 52, "months": 4.33, "weeks": 1, "days": 1 / 7},
    "days": {"years": 365, "months": 30.4, "weeks": 7, "days": 1},
}
UNIT_WORDS = {
    "years": "years", "year": "years", "yrs": "years", "yr": "years", "y": "years",
    "months": "months", "month": "months", "mths": "months", "mth": "months", "mo": "months",
    "weeks": "weeks", "week": "weeks", "wks": "weeks", "wk": "weeks",
    "days": "days", "day": "days", "d": "days",
}
UNIT_ORDER = ["years", "months", "weeks", "days"]  # tie-break for the most common unit

KEEP_CASE = {"genus", "scientific_name", "fire_response_categorical_surv1", "fire_response_implied",
             "file_name", "notes", "data_quote", "pdf_path"}
DASH_RE = re.compile(r"[‐-―−]")  # hyphen variants, en/em dash, minus sign
TIME_RE = re.compile(r"[<>]?\d+(\.\d+)?(-\d+(\.\d+)?)?")
RAW_TIME_RE = re.compile(r"(.+?)\s*([A-Za-z]+)\.?")
NUMBER_RE = re.compile(r"\d+(\.\d+)?")


def columns_from_claude_md():
    """COLUMNS list from CLAUDE.md, as in check.py."""
    text = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
    block = text[text.index("COLUMNS = ["):]
    block = block[:block.index("\n]")]
    return re.findall(r'^\s+\("([^"]+)", "', block, re.M)


def parse_time(cell):
    """'3.0 - 16.0 years' -> ('3.0-16.0', 'years'); None if not '<value> <unit>'."""
    m = RAW_TIME_RE.fullmatch(DASH_RE.sub("-", cell.strip()))
    if not m or m.group(2).lower() not in UNIT_WORDS:
        return None
    value = re.sub(r"\s+", "", m.group(1))
    if not TIME_RE.fullmatch(value):
        return None
    return value, UNIT_WORDS[m.group(2).lower()]


def fmt(x):
    """Round to 3 decimals, drop trailing zeros: 2.1666 -> '2.167', 4.0 -> '4'."""
    return f"{round(x, 3):.3f}".rstrip("0").rstrip(".")


def convert(value, unit, target):
    """Convert a time value ('26', '>4', '3.0-16.0') from unit to target; printed value kept if no conversion."""
    if unit == target:
        return value
    f = FACTOR[target][unit]
    return NUMBER_RE.sub(lambda m: fmt(float(m.group(0)) * f), value)


def convert_error(value, f):
    """Scale every number in an error value (se, sd, ci 'lower-upper', negative bounds included)."""
    return re.sub(r"\d+(\.\d+)?", lambda m: fmt(float(m.group(0)) * f), value)


def normalise_row(row, problems, where):
    out = dict(row)
    for col, value in out.items():
        value = value.strip()
        if col != "data_quote":
            value = DASH_RE.sub("-", value)
        out[col] = value
    if out["genus"] == "NA":  # NA row: only pdf_path to fill
        out["pdf_path"] = pdf_path(out["file_name"], problems, where)
        return out

    for col in FILLED_HERE:
        if out[col]:
            problems.append(f"{where}: {col} must be empty in raw (filled here); raw value replaced: {out[col]}")
            out[col] = ""

    notes = []      # conversion notes, written before the agent's notes
    factors = {}    # column -> factor applied, for error_value

    def parsed(col):
        if not out[col]:
            return None
        p = parse_time(out[col])
        if p is None:
            problems.append(f"{where}: {col} not '<value> <unit>'; cell left empty, raw value in notes: {out[col]}")
            notes.append(f"{col} raw value not parsed: {out[col]}")
            out[col] = ""
        return p

    def to(col, value, unit, target):
        out[col] = convert(value, unit, target)
        if unit != target:
            notes.append(f"{col} converted from {value} {unit}")
            factors[col] = FACTOR[target][unit]

    #fixed years columns (repr4 here only when the agent filled it: maturation age)
    for col in YEARS_COLS:
        p = parsed(col)
        if p:
            to(col, p[0], p[1], "years")

    #primary juvenile period: months -> pjp_mths (+ repr4 = months / 12); other units -> years
    p = parsed(PJP)
    repr4 = "time_to_50_percent_flowering_repr4"
    if p and p[1] == "months":
        out["pjp_mths"], out[PJP] = p[0], ""
        if out["error_column"] == PJP:
            out["error_column"] = "pjp_mths"
        if out[repr4]:
            problems.append(f"{where}: {repr4} filled in raw (maturation age) and derivable from pjp_mths; raw value kept: {out[repr4]}")
        else:
            out[repr4] = convert(p[0], "months", "years")  # no notes entry (metadata.csv rule)
    elif p:
        to(PJP, p[0], p[1], "years")

    #variable-unit columns: one unit per row, in time_unit
    vals = {col: parsed(col) for col in VARIABLE_COLS}
    vals = {col: p for col, p in vals.items() if p}
    if vals:
        units = Counter(u for _, u in vals.values())
        target = VARIABLE_UNIT_TARGET or max(UNIT_ORDER, key=lambda u: (units[u], -UNIT_ORDER.index(u)))
        for col, (value, unit) in vals.items():
            to(col, value, unit, target)
        out["time_unit"] = target

    #error value is in the unit of its time column as printed
    err_col = out["error_column"]
    if out["error_value"] not in ("", "NA") and err_col in factors:
        notes.append(f"error_value converted from {out['error_value']} (with {err_col})")
        out["error_value"] = convert_error(out["error_value"], factors[err_col])

    #case, names, path
    for col, value in out.items():
        if col not in KEEP_CASE and not (col == "source" and value == out["file_name"]):
            out[col] = value.lower()
    out["genus"] = out["genus"][:1].upper() + out["genus"][1:].lower()
    out["scientific_name"] = f"{out['genus']} {out['species']}".strip()
    out["pdf_path"] = pdf_path(out["file_name"], problems, where)
    out["notes"] = "; ".join(filter(None, notes + [out["notes"]]))
    return out


def pdf_path(stem, problems, where):
    path = PDF_CLEAN + f"{stem}.pdf"
    if not (REPO / path).exists():
        problems.append(f"{where}: no PDF {path}; pdf_path left empty")
        return ""
    return path


def main():
    slugs = sys.argv[1:] or sorted(p.name[:-len("_raw.csv")] for p in RESULTS.glob("*_raw.csv"))
    columns = columns_from_claude_md()
    for slug in slugs:
        raw_path, out_path = RESULTS / f"{slug}_raw.csv", RESULTS / f"{slug}.csv"
        with open(raw_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != columns:
                sys.exit(f"{raw_path.relative_to(REPO)}: header must be the {len(columns)} COLUMNS names in CLAUDE.md")
            raw = list(reader)
        problems = []
        rows = [normalise_row(r, problems, f"raw line {i}") for i, r in enumerate(raw, 2)]
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        n_conv = sum("converted from" in r["notes"] for r in rows)
        print(f"{slug}: {len(rows)} rows -> {out_path.relative_to(REPO)} | rows with conversions {n_conv} | problems {len(problems)}")
        for p in problems:
            print(f"    {p}")


if __name__ == "__main__":
    main()
