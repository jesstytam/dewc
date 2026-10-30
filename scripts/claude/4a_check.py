"""Check extraction output against the rules in CLAUDE.md.

Usage (from the repo root):
    python scripts/claude/4a_check.py <slug> --paper <stem>   # after each paper in Step 1 (raw results)
    python scripts/claude/4a_check.py <slug>                  # after all papers in Step 1 (raw results)
    python scripts/claude/4a_check.py <slug> --final          # after scripts/pipeline/5_normalise.py (final results)
    python scripts/claude/4a_check.py --step0                 # after Step 0

Only checks that need no reading of the paper; column rules are in references/metadata.csv.
Row checks are pydantic models whose fields are the metadata.csv columns. Never edits RESULT or LOG.
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

from pydantic import ConfigDict, Field, ValidationError, create_model, field_validator
from pydantic_core import PydanticCustomError

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "data/inference_test"  # test run only; never data/inference
MD_RAW = REPO / "data/papers_test/md_raw"
MD_LLM = REPO / "data/papers_test/md_llm"
PDF_CLEAN = "data/papers_test/pdf_clean/"
PDF_CLEAN_DIR = REPO / PDF_CLEAN
LOGS = ROOT / "logs"
METADATA = ROOT / "references/metadata.csv"  # column dictionary; the row models are built from it

TOKEN_COLS = ["n_requests", "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "total_tokens"]
LOG_HEADER = ["paper", "status", "n_rows", "started", "finished", "note"] + TOKEN_COLS
MD_LOG_HEADER = ["paper", "status", "pdf_pages", "n_tables", "n_fixes", "unresolved", "started", "finished", "note"] + TOKEN_COLS
STATUSES = {"done", "broken", "no_data"}
MD_STATUSES = {"done", "text_layer", "no_pdf"}

FIXED_YEARS = [
    "age_at_first_flower_production_from_seed_repr3",
    "time_to_first_flower_production_resprout_repr3a",
    "time_to_50_percent_flowering_repr4",
]
VARIABLE_UNIT = [
    "secondary_juvenile_period",
    "time_to_50_percent_flowering",
    "time_to_80_percent_flowering",
    "recovery_time",
]
TIME_COLS = ["pjp_mths", "primary_juvenile_period"] + FIXED_YEARS + VARIABLE_UNIT
UNIT_OF = {col: col + "_unit" for col in TIME_COLS if col != "pjp_mths"}  # time column -> its unit column
RAW_EMPTY = ["pjp_mths", "scientific_name", "pdf_path"]  # filled by 5_normalise.py

TIME_RE = re.compile(r"[<>]?\d+(\.\d+)?(-\d+(\.\d+)?)?")
NUMBER_RE = re.compile(r"-?\d+(\.\d+)?")
SEASON_RE = re.compile(r"(summer|autumn|winter|spring)(; (summer|autumn|winter|spring))*")
SEASON_ORDER = ["summer", "autumn", "winter", "spring"]
ERROR_TYPE_RE = re.compile(r"se|sd|ci\d+|± not defined")
ERROR_NUMBER_RE = re.compile(r"\d+(\.\d+)?")
CI_RE = re.compile(r"-?\d+(\.\d+)?--?\d+(\.\d+)?|-?\d+(\.\d+)?-\d+(\.\d+)?")
SUPP_RE = re.compile(r"supplementary|supporting information|online resource|electronic supplement|\b(table|fig\.?|figure|appendix) s\d", re.I)
KEEP_CASE = {"genus", "scientific_name", "fire_response_categorical_surv1", "fire_response_implied", "file_name", "notes", "data_quote", "pdf_path"}  # see Case in CLAUDE.md; notes quote codes, genus names and printed forms; data_quote is verbatim
PLURAL_RE = re.compile(r"\b[a-z]+[^s\W]s\b")  # e.g. rhizomes, tubers (not grass)
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
APA_RE = re.compile(r"[^()]+ \((\d{4}[a-z]?|n\.d\.)\)\. .+")  # (n.d.) = no year printed
LOC_PAGE_RE = re.compile(r"\b(pdf )?p\. \d")
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
    """Same as: sha256sum data/papers_test/md_llm/*.md | LC_ALL=C sort | sha256sum (from the repo root)."""
    lines = sorted(f"{sha256_hex(p.read_bytes())}  {p.relative_to(REPO)}\n" for p in MD_LLM.glob("*.md"))
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
    """Token cells: empty (agent) or whole numbers (filled by 4c_usage.py)."""
    for col in TOKEN_COLS:
        if entry.get(col, "") and not entry[col].isdigit():
            report.error(where, col, "empty or whole number; filled by 4c_usage.py", entry[col])


def decimals(value):
    return len(value.split(".")[1]) if "." in value else 0


def squash(text):
    return " ".join(text.split())


_paper_text = {}


def paper_text(stem):
    """Paper markdown with whitespace runs squashed, or None if missing."""
    if stem not in _paper_text:
        md = MD_LLM / f"{stem}.md"
        _paper_text[stem] = squash(md.read_text(encoding="utf-8")) if md.exists() else None
    return _paper_text[stem]


def check_quote(row):
    """data_quote: one '[<data_location item>] <quote>' per data_location item, each quote found verbatim in the paper."""
    loc, quote = row["data_location"], row["data_quote"]
    if not quote:
        yield error("verbatim quote for each data_location item, e.g. '[table 2, p. 342] | Banksia ericifolia | R | 5 |'", quote)
        return
    if not loc:
        return
    items = loc.split("; ")
    starts = []
    pos = 0
    for k, item in enumerate(items):
        tag = f"[{item}] "
        at = quote.lower().find((tag if k == 0 else "; " + tag).lower(), pos)  # data_location is lower-cased by 5_normalise.py
        if at == -1 or (k == 0 and at != 0):
            yield error(f"item {k + 1} must start with '[{item}] ' (one item per data_location item, same order, joined by '; ')", quote[:120])
            return
        starts.append((at if k == 0 else at + 2, len(tag)))
        pos = at + len(tag)
    text = paper_text(row["file_name"])
    if text is None:
        return
    for k, (at, n) in enumerate(starts):
        end = starts[k + 1][0] - 2 if k + 1 < len(starts) else len(quote)
        body = quote[at + n:end]
        for piece in body.split(" ... "):
            piece = squash(piece)
            if piece and piece not in text:
                yield error(f"not found verbatim in the paper ([{items[k]}]); copy it from the markdown", piece[:120])


def expected_pdf_path(stem):
    """pdf_path rule in metadata.csv: the PDF in pdf_clean with the paper's file stem."""
    return PDF_CLEAN + f"{stem}.pdf" if (PDF_CLEAN_DIR / f"{stem}.pdf").exists() else ""


def formatted(row):
    """Raw row with the case and dash rules applied, as 5_normalise.py does, for the content checks."""
    out = {}
    for col, value in row.items():
        if col != "data_quote":
            value = DASH_RE.sub("-", value)
        if value != "NA" and col not in KEEP_CASE and not (col == "source" and value == row["file_name"]):
            value = value.lower()
        out[col] = value
    if out["genus"] != "NA":
        out["genus"] = out["genus"][:1].upper() + out["genus"][1:].lower()
    return out


def raw_time_ok(value):
    """Value as printed: number, min-max or >/< bound, e.g. '26', '3.0 - 16.0', '>4'."""
    return bool(TIME_RE.fullmatch(re.sub(r"\s+", "", DASH_RE.sub("-", value))))


# Row rules: one pydantic model per row kind (data row, NA row), its fields built from references/metadata.csv.
# Each rule is a generator registered with @rule for the columns it reports on; it gets the row after the
# case and dash rules (formatted) and yields error(...) or warning(...). Every field is validated on its own,
# so a row reports all its problems at once, each on the column it belongs to.

RULES = []  # (columns, row kinds, function); "*" = every column


def rule(*columns, rows=("data",)):
    def add(f):
        RULES.append((columns, rows, f))
        return f
    return add


def error(check, value=""):
    return ("error", check, value)


def warning(check, value=""):
    return ("warning", check, value)


@rule("*", rows=("data", "na"))
def cell_format(col, value, row, ctx):
    orig = ctx["orig"][col]
    if orig != orig.strip():
        yield error("leading or trailing space", orig)
    if ctx["raw"]:
        return  # case and dashes are set by 5_normalise.py
    if DASH_RE.search(orig) and col != "data_quote":
        yield error("en or em dash; use ASCII hyphen '-'", orig)
    if orig != "NA" and orig != orig.lower() and col not in KEEP_CASE:
        if not (col == "source" and orig == row["file_name"]):
            yield error("lower case (only genus, codes and file_name keep capitals)", orig)


@rule("source", "file_name", rows=("data", "na"))
def required(col, value, row, ctx):
    if not value or value == "NA":
        yield error("empty or NA")


@rule(*RAW_EMPTY)
def raw_empty(col, value, row, ctx):
    if ctx["raw"] and value:
        yield error("leave empty in raw results: 5_normalise.py fills it", ctx["orig"][col])


@rule("pdf_path", rows=("data", "na"))
def pdf_path(col, value, row, ctx):
    if not ctx["raw"]:
        pdf = expected_pdf_path(row["file_name"])
        if value != pdf:
            yield error(f"must be '{pdf}'" if pdf else "no PDF with this file stem in pdf_clean", value)


@rule("*", rows=("na",))
def na_cell(col, value, row, ctx):
    keep = ("notes", "source", "file_name", "supplementary_material") + (() if ctx["raw"] else ("pdf_path",))
    if col not in keep and value != "NA":
        yield error("NA row: cell must be NA", value)
    if col == "notes" and (not value or value == "NA"):
        yield error("NA row: reason missing")


@rule("*")
def no_na(col, value, row, ctx):
    if value == "NA":
        yield error("NA in data row; leave empty instead")


@rule("genus", "species", "subsp")
def name(col, value, row, ctx):
    if col != "subsp" and not value:
        yield error("empty")
    if NAME_MARK_RE.search(value):
        yield error("remove '?' or '*' from the name; printed form in Notes", value)
    if HYPHEN_SPACE_RE.search(value):
        yield error("space next to a hyphen; hyphenated epithet is one word ('novae- zelandiae' -> 'novae-zelandiae')", value)
    if col == "genus" and value and not re.fullmatch(r"[A-Z][a-z]+", value):
        yield error("one capitalised word, no marks", value)
    if col == "species":
        if RANK_IN_SPECIES_RE.search(value):
            yield error("rank word in Species; rank and name go in subsp", value)
        elif value and not re.fullmatch(r"[a-z][a-z-]*", value):
            yield warning("not a plain lower-case epithet (fine for phrase names, e.g. 'sp. A')", value)
    if col == "subsp" and value and not RANK_RE.match(value):
        yield error("rank word + name, e.g. 'subsp. buxifolia', 'var. lanceolatus', 'f. glauca'", value)


@rule("scientific_name")
def scientific_name(col, value, row, ctx):
    name = f"{row['genus']} {row['species']}"
    if not ctx["raw"] and value != name:
        yield error(f"must be genus + ' ' + species: '{name}'", value)


@rule("native_status")
def native_status(col, value, row, ctx):
    if value and not re.fullmatch(r"[a-z]+( [a-z]+)*", value):
        yield error("paper's term in lower case, e.g. native, exotic", value)


@rule("fire_response_categorical_surv1", "fire_response_implied")
def fire_response(col, value, row, ctx):
    if CODE_SPACE_RE.search(value):
        yield error("space next to '?', '/', ';', ',' or a bracket; remove it ('? r' -> '?r')", value)
    if col == "fire_response_implied" and value not in ("", "NA") and row["fire_response_categorical_surv1"] not in ("", "NA"):
        yield error("fill only when fire_response_categorical_surv1 is empty (stated response wins)", value)


@rule("source")
def source(col, value, row, ctx):
    if value != row["file_name"] and not APA_RE.fullmatch(value):
        yield warning("does not look like APA: 'author, a. b. (yyyy). title. ...'", value)


@rule("data_location")
def data_location(col, value, row, ctx):
    if not value:
        yield error("where the row's values are printed, e.g. 'table 2, p. 342'", value)
    elif value != "NA" and not LOC_PAGE_RE.search(value):
        yield warning("no page: add 'p. N' (printed page) or 'pdf p. N'", value)


@rule("data_quote")
def data_quote(col, value, row, ctx):
    yield from check_quote(row)


@rule("notes")
def notes(col, value, row, ctx):
    m = NOTES_PAGE_RE.search(value)
    if m:
        yield warning("page reference: write 'p. N' (printed page) or 'pdf p. N'", m.group(0))


@rule("latitude", "longitude")
def coordinate(col, value, row, ctx):
    lo, hi = {"latitude": (-44, -10), "longitude": (112, 154)}[col]
    if not value:
        return
    if not NUMBER_RE.fullmatch(value):
        yield error("not a decimal number", value)
    elif not lo <= float(value) <= hi:
        yield error(f"outside {lo} to {hi}", value)
    elif "." in value and (value.endswith("0") or decimals(value) > 4):
        yield error("at most 4 decimals, no trailing zeros ('151.0' -> '151')", value)


@rule(*TIME_COLS)
def time_value(col, value, row, ctx):
    if not value:
        return
    if ctx["raw"]:
        if col not in RAW_EMPTY and not raw_time_ok(value):
            yield error("value as printed: number, min-max or >/< bound, e.g. '26', '>4'; unit in its _unit column", value)
        return
    if not TIME_RE.fullmatch(value):
        yield error("time format: number, min-max, or >/< bound", value)
    elif col in FIXED_YEARS and any(decimals(part) > 3 for part in value.lstrip("<>").split("-")):
        yield error("more than 3 decimals", value)


@rule(*UNIT_OF.values())
def time_unit(col, value, row, ctx):
    time_col = col[:-len("_unit")]
    if row[time_col] and value not in ctx["allowed"][col]:
        yield error(f"unit of {time_col}: days, weeks, months or years", value)
    elif not row[time_col] and value:
        yield error(f"must be empty: {time_col} is empty", value)
    elif not ctx["raw"] and value and time_col in FIXED_YEARS + ["primary_juvenile_period"] and value != "years":
        yield error("final results: years (5_normalise.py converts)", value)


@rule("error_column", "error_type", "error_value")
def error_cells(col, value, row, ctx):
    err_col, err_type, err_value = row["error_column"], row["error_type"], row["error_value"]
    filled = err_value not in ("", "NA")
    if col == "error_column" and filled:
        if err_col not in TIME_COLS:
            yield error("name of the time column the error belongs to", err_col)
        elif not row[err_col]:
            yield error("names an empty time column", err_col)
    if col == "error_type":
        if filled and not err_type:
            yield error("needed when error_value is filled", err_type)
        if err_type not in ("", "NA") and not ERROR_TYPE_RE.fullmatch(err_type):
            yield warning("not se, sd, ci<N> or '± not defined'; fine if printed so", err_type)
    if col == "error_value":
        if filled:
            if err_type.startswith("ci") and not CI_RE.fullmatch(err_value):
                yield error("confidence interval as lower-upper, e.g. 1.5-3.7", err_value)
            elif err_type in ("se", "sd") and not ERROR_NUMBER_RE.fullmatch(err_value):
                yield error("se or sd: a single number", err_value)
        elif (err_col or err_type) and "NA" not in (err_col, err_type):
            yield error("empty, but error_column or error_type is filled", err_value)


@rule("sample_size")
def sample_size(col, value, row, ctx):
    if value not in ("", "NA") and not re.fullmatch(r"\d+", value):
        yield warning("not a whole number; fine if printed so (explain in notes)", value)


@rule("fire_season_categorical")
def fire_season(col, value, row, ctx):
    if not value:
        return
    seasons = value.split("; ")
    order = ctx["allowed"]["fire_season_categorical"]
    if any(s not in order for s in seasons):
        yield error("summer|autumn|winter|spring, joined by '; '", value)
    elif seasons != sorted(seasons, key=order.index):
        yield error("calendar order: summer; autumn; winter; spring", value)


@rule("resprouter_type", "location_name")
def several_values(col, value, row, ctx):
    if col == "resprouter_type":
        if re.search(r"\b(and|or)\b", value):
            yield warning("several types: join with '; ' instead of 'and' / 'or'", value)
        if value != value.lower() or PLURAL_RE.search(value):
            yield warning("lower case and singular, e.g. rhizome, lignotuber", value)
    if re.search(r"\s/\s", value) or (col == "resprouter_type" and "/" in value):
        yield warning("several values: join with '; ' (keep '/' only if printed inside one value)", value)


@rule("rainfall_mm", "rainfall_post_fire_mm")
def rainfall(col, value, row, ctx):
    if value and value != "NA" and not re.fullmatch(r"\d+(\.\d+)?(-\d+(\.\d+)?)?", value):
        yield error("not a number or min-max range", value)


@rule("rainfall_post_fire_period")
def rainfall_period(col, value, row, ctx):
    if bool(row["rainfall_post_fire_mm"]) != bool(value):
        yield error("rainfall_post_fire_mm and its period go together", value)


def metadata():
    """Column dictionary rows of references/metadata.csv, in column order."""
    return list(csv.DictReader(open(METADATA, encoding="utf-8", newline="")))


def closed_values(meta):
    """allowed_values of the columns with a closed list (no 'as printed'), in their printed order."""
    out = {}
    for m in meta:
        values = [v.strip() for v in m["allowed_values"].split(" | ") if v.strip()]
        if values and "as printed" not in values and not any(" " in v for v in values):
            out[m["column"]] = values
    return out


def run_rules(rules):
    def validate(cls, value, info):
        ctx, errors = info.context, []
        for f in rules:
            for level, check, shown in f(info.field_name, value, ctx["row"], ctx):
                if level == "error":
                    errors.append((check, shown))
                else:
                    ctx["warnings"].append((info.field_name, check, shown))
        if errors:
            raise PydanticCustomError("row_rule", "{checks}", {"checks": errors})
        return value
    return validate


def build_model(name, kind, meta):
    """Pydantic model of one row kind: 1 str field per metadata column, with the rules registered for that kind."""
    fields = {m["column"]: (str, Field(description=m["definition"])) for m in meta}
    validators = {}
    for col in fields:
        rules = [f for cols, kinds, f in RULES if kind in kinds and (col in cols or cols == ("*",))]
        if rules:
            validators[f"check_{col}"] = field_validator(col)(run_rules(rules))
    return create_model(name, __config__=ConfigDict(extra="forbid"), __validators__=validators, **fields)


_models = {}


def row_models():
    if not _models:
        meta = metadata()
        _models.update(data=build_model("DataRow", "data", meta), na=build_model("NaRow", "na", meta),
                       allowed=closed_values(meta))
    return _models


def check_row(line, row, report, raw=True):
    where = f"RESULT line {line}"
    models = row_models()
    kind = "na" if row["genus"] == "NA" else "data"
    ctx = {"raw": raw, "orig": row, "row": formatted(row) if raw else row, "allowed": models["allowed"], "warnings": []}
    try:
        models[kind].model_validate(ctx["row"], context=ctx)
    except ValidationError as e:
        for err in e.errors():
            col = str(err["loc"][0]) if err["loc"] else ""
            if err["type"] == "row_rule":
                for check, shown in err["ctx"]["checks"]:
                    report.error(where, col, check, shown)
            else:  # column missing from or not in metadata.csv
                report.error(where, col, err["msg"], str(err.get("input", ""))[:120])
    for col, check, shown in ctx["warnings"]:
        report.warn(where, col, check, shown)


def check_step1(slug, paper, report, final=False):
    columns = columns_from_claude_md()
    result_path = ROOT / (f"results/{slug}.csv" if final else f"results/{slug}_raw.csv")
    log_path = LOGS / f"{slug}_log.csv"
    result = read_csv(result_path, report, "RESULT")
    log = read_csv(log_path, report, "LOG")
    if result is None or log is None:
        return

    # file level
    if not result or result[0] != columns:
        report.error("RESULT line 1", "", f"header must be the {len(columns)} COLUMNS names in order")
        return
    if [m["column"] for m in metadata()] != columns:
        report.error("METADATA", "column", "metadata.csv columns differ from COLUMNS in CLAUDE.md; row checks need both the same")
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
        expected = sorted(p.stem for p in MD_LLM.glob("*.md"))
        counts = Counter(r["paper"] for r in papers)
        for stem in expected:
            if counts[stem] != 1:
                report.error("LOG", "paper", f"{counts[stem]} LOG lines, expected 1", stem)
        for stem in counts:
            if stem not in expected:
                report.error("LOG", "paper", "not a file in PAPERS", stem)

    stems = {r["paper"] for r in log_rows if r["paper"] != "_run"}
    for line, row in rows:
        if row["file_name"] not in stems:
            report.error(f"RESULT line {line}", "file_name", "matches no LOG paper", row["file_name"])

    # paper level
    checked_stems = set()
    for r in papers:
        where = f"LOG {r['paper']}"
        if r["status"] not in STATUSES:
            report.error(where, "status", "must be done, broken or no_data", r["status"])
        check_times(where, r, report)
        check_tokens(where, r, report)
        checked_stems.add(r["paper"])
        paper_rows = [(line, row) for line, row in rows if row["file_name"] == r["paper"]]
        supp = {row["supplementary_material"] for _, row in paper_rows}
        if len(supp) > 1:
            report.error(where, "supplementary_material", f"{len(supp)} different strings; use one on every row", " | ".join(sorted(supp)))
        md = MD_LLM / f"{r['paper']}.md"
        if md.exists() and supp <= {"", "NA"}:
            m = SUPP_RE.search(md.read_text(encoding="utf-8"))
            if m:
                report.warn(where, "supplementary_material", "paper refers to supplementary material; fill '<item> (<content>)' on every row", m.group(0))
        if not paper_rows:
            report.error(where, "", "no rows in RESULT")
        if str(len(paper_rows)) != r["n_rows"]:
            report.error(where, "n_rows", f"RESULT has {len(paper_rows)} rows", r["n_rows"])
        if r["status"] in ("broken", "no_data") and not any(row["genus"] == "NA" for _, row in paper_rows):
            report.error(where, "status", f"{r['status']} paper needs an NA row")
        citations = {row["source"] for _, row in paper_rows}
        if len(citations) > 1:
            report.error(where, "source", f"{len(citations)} different Source strings; use one", " | ".join(sorted(citations)))

    # row level (duplicate rows are allowed; handled after extraction)
    checked = [(line, row) for line, row in rows if paper is None or row["file_name"] in checked_stems]
    for line, row in checked:
        check_row(line, row, report, raw=not final)
    # location_name empty on some rows of a paper while other rows name a site: usually a missed site
    by_paper = {}
    for line, row in checked:
        if row["genus"] != "NA":  # NA rows are checked in check_row
            by_paper.setdefault(row["file_name"], []).append((line, row))
    for stem, prow in by_paper.items():
        empty = [line for line, row in prow if not row["location_name"]]
        if empty and len(empty) < len(prow):
            report.warn(f"RESULT lines {empty[0]}..{empty[-1]}", "location_name",
                        f"empty on {len(empty)} of {len(prow)} rows of {stem} while other rows name a site; fill it, or say in notes why the row has no site",
                        "")


def check_step0(report):
    log = read_csv(LOGS / "md_opt_log.csv", report, "MD_LOG")
    if log is None:
        return
    if not log or log[0] != MD_LOG_HEADER:
        report.error("MD_LOG line 1", "", "header must be " + ",".join(MD_LOG_HEADER))
        return
    log_rows = [dict(zip(MD_LOG_HEADER, cells)) for cells in log[1:]]
    counts = Counter(r["paper"] for r in log_rows)

    # Step 0 moves or removes every md_raw file once its md_llm file is finished
    for md in sorted(MD_RAW.glob("*.md")):
        report.error(f"MD_RAW {md.stem}", "", "still in md_raw: Step 0 not finished for this paper")

    for out in sorted(MD_LLM.glob("*.md")):
        stem, where = out.stem, f"MD_LLM {out.stem}"
        if counts[stem] != 1:
            report.error("MD_LOG", "paper", f"{counts[stem]} lines, expected 1", stem)
        if not (PDF_CLEAN_DIR / f"{stem}.pdf").exists():
            report.warn(where, "", "no PDF with the same stem in pdf_clean")
        text = out.read_text(encoding="utf-8")
        lines = text.rstrip().splitlines()
        if not lines or not lines[-1].startswith("<!-- md_opt:"):
            report.error(where, "", "no <!-- md_opt: end comment")
        if "<!-- pdf2md:" in text:
            report.error(where, "", "<!-- pdf2md: ... --> line copied from md_raw; remove it")
        entry = next((r for r in log_rows if r["paper"] == stem), None)
        if entry:
            if entry["status"] not in MD_STATUSES:
                report.error(f"MD_LOG {stem}", "status", "must be " + ", ".join(sorted(MD_STATUSES)), entry["status"])
            check_times(f"MD_LOG {stem}", entry, report)
            check_tokens(f"MD_LOG {stem}", entry, report)
        if entry and entry["status"] == "text_layer":
            continue  # moved unchanged; no optimisation checks
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
    parser.add_argument("--final", action="store_true", help="check the final results written by 5_normalise.py instead of the raw results")
    args = parser.parse_args()
    if not args.step0 and not args.slug:
        parser.error("give a slug, or --step0")

    report = Report()
    if args.step0:
        check_step0(report)
        out = LOGS / "md_opt_check.csv"
        scope = "Step 0"
    else:
        check_step1(args.slug, args.paper, report, args.final)
        out = LOGS / (f"{args.slug}_check_final.csv" if args.final else f"{args.slug}_check.csv")
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
