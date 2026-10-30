"""Score Step 1 results against the human-extracted answers (accuracy benchmark).

Usage (from the repo root):
    python scripts/claude/6_benchmark.py              # score every Step 1 snapshot in logs/runs/ not yet in benchmark.csv
    python scripts/claude/6_benchmark.py --rescore    # score all snapshots again
    python scripts/claude/6_benchmark.py --run <dir>  # score one snapshot folder
    python scripts/claude/6_benchmark.py --taxa       # list every taxon name for scripts/claude/6a_taxon_map.R
    python scripts/claude/6_benchmark.py --report     # per-paper and per-column scores (latest run of each paper), with metrics

Taxon names: when logs/benchmark_taxon_map.csv exists (6a_taxon_map.R, APCalign), names on both sides are first
replaced by their APC accepted names, so a synonym is not 1 miss + 1 extra; names without one stay as printed.
Rerun --taxa and 6a_taxon_map.R after new runs or answer changes; new names are compared as printed until then.

Ground truth: data/papers_test/answers/juvenile_period_data_part*.ods, first sheet of each (agents never read it).
Answer rows are matched to papers by Path (the paper's PDF in pdf_clean; its file stem = file_name in the results);
papers without answer rows are not scored.
Only papers extracted in the run itself are scored (LOG started >= the run's last _run line), so papers
carried over from an earlier run are not counted twice.

Two levels, each with true positives (tp), false positives (fp) and false negatives (fn):
  record: taxa (genus + species + subsp) per paper. tp = taxon in both; fp = model only; fn = answers only.
  value:  for each taxon in both, the set of values of a column over the taxon's rows.
          tp = values in both; fp = model values not in the answers (wrong or extra); fn = answer values the model lacks.
Scores: precision, recall, f1, and f05 (F0.5: precision weighted twice as much as recall; headline score).
  fp_extra: the part of fp where the answer cell is empty. The checked answers leave a cell empty only when
  the paper does not state the value, so these are model errors and count in precision; the split is kept to
  separate invented values from wrong ones. precision_filled = tp / (tp + fp - fp_extra), i.e. precision over
  cells both sides filled.

Writes, under data/inference_test/logs/:
  benchmark.csv          1 line per run x paper x level x column, plus totals (paper "_all", column "_all");
                         joins sessions.csv on (session_id, step)
  benchmark_papers.csv   per agent, the latest scored run of each paper (by start time in sessions.csv), plus totals
  benchmark_details.csv  1 line per taxon or value in only one side, and per taxon matched through a synonym (kind 'synonym'), with the model's source location (data_location; notes in older runs)
"""

import argparse
import csv
import hashlib
import importlib.util
import re
import sys
import zipfile
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree

REPO = Path(__file__).resolve().parents[2]
LOGS = REPO / "data/inference_test/logs"
RUNS = LOGS / "runs"
ANSWERS = sorted((REPO / "data/papers_test/answers").glob("juvenile_period_data_part*.ods"))
# partN_updated.ods supersedes partN.ods when both are present
ANSWERS = [p for p in ANSWERS if not p.with_name(p.stem + "_updated.ods").exists()]
OUT = LOGS / "benchmark.csv"
DETAILS = LOGS / "benchmark_details.csv"
TAXA = LOGS / "benchmark_taxa.csv"  # every taxon name in the answers and the runs (--taxa); input of 6a_taxon_map.R
TAXON_MAP = LOGS / "benchmark_taxon_map.csv"  # APC accepted name of each name in TAXA (6a_taxon_map.R)
PAPERS_OUT = LOGS / "benchmark_papers.csv"  # latest score of each paper per agent
SESSIONS = LOGS / "sessions.csv"
FIRE_PCT = REPO / "data/inference_test/references/fire_response_pct.csv"  # fire response code -> class (obligate, O/R, resprouter)

# answer column (old name) -> result column (new name); scored at the value level
VALUE_COLS = {
    "PJP mths": "pjp_mths",
    "Time to 50% flowering_repr4": "time_to_50_percent_flowering_repr4",
    "Age at first flower production from seed_repr3": "age_at_first_flower_production_from_seed_repr3",
    "Time to first flower production resprout_repr3a": "time_to_first_flower_production_resprout_repr3a",
    "primary_juvenile_period": "primary_juvenile_period",
    "secondary_juvenile_period": "secondary_juvenile_period",
    "time_to_50_percent_flowering": "time_to_50_percent_flowering",  # new column; scored once the answers have it
    "fire_response categorical_surv1": "fire_response_categorical_surv1",
    "resprouter_type": "resprouter_type",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Rainfall_mm": "rainfall_mm",
    "Fire_season_categorical": "fire_season_categorical",
    "Fire_severity_categorical": "fire_severity_categorical",
}
# how each scored column is compared (values of a taxon pooled over its rows into a set on each side)
METRICS = {
    "taxon": "genus + species + subsp, lower case, marks removed; APC accepted name when mapped; else Levenshtein <= 2 within genus",
    "pjp_mths": "number, range or >/< bound, marks (c., ~, ?) removed; within half a unit of the coarser printed precision, at most 0.05",
    "time_to_50_percent_flowering_repr4": "number, range or >/< bound, marks (c., ~, ?) removed; within half a unit of the coarser printed precision, at most 0.05",
    "age_at_first_flower_production_from_seed_repr3": "number, range or >/< bound, marks (c., ~, ?) removed; within half a unit of the coarser printed precision, at most 0.05",
    "time_to_first_flower_production_resprout_repr3a": "number, range or >/< bound, marks (c., ~, ?) removed; within half a unit of the coarser printed precision, at most 0.05",
    "primary_juvenile_period": "number, range or >/< bound, marks (c., ~, ?) removed; within half a unit of the coarser printed precision, at most 0.05",
    "secondary_juvenile_period": "as above, after conversion to years (answers are in years)",
    "time_to_50_percent_flowering": "as above, after conversion to years (answers are in years)",
    "rainfall_mm": "each number (range bounds separately), marks removed; within half a unit of the coarser precision, at most 0.05",
    "latitude": "decimal degrees as printed; equal within 0.01",
    "longitude": "decimal degrees as printed; equal within 0.01",
    "fire_response_categorical_surv1": "class obligate, O/R or resprouter (references/fire_response_pct.csv; paper's own code definition first, then standard class): equal when classes match; codes without a class exact",
    "resprouter_type": "each term (split on ; / , and or), lower case, singular; exact",
    "fire_season_categorical": "all seasons of the cell, sorted and joined; exact",
    "fire_severity_categorical": "each term (split on ; / , and or), lower case; exact",
    "introduced": "flag: native_status introduced/exotic/naturalised/weed or '*' in the name",
}
NUMERIC = {"pjp_mths", "time_to_50_percent_flowering_repr4", "age_at_first_flower_production_from_seed_repr3",
           "time_to_first_flower_production_resprout_repr3a", "primary_juvenile_period", "secondary_juvenile_period",
           "time_to_50_percent_flowering",
           "rainfall_mm"}
COORDS = {"latitude", "longitude"}
VARIABLE_UNIT = {"secondary_juvenile_period", "time_to_50_percent_flowering"}  # unit in time_unit; converted to years
YEARS_PER = {"days": 1 / 365, "weeks": 1 / 52, "months": 1 / 12, "years": 1}
INTRODUCED = {"introduced", "exotic", "naturalised", "naturalized", "weed"}

SKIP = {  # snapshots that are not runs of their own
    "277cfa7d-2629-481f-9e22-0fbcaef68be6": "stray session that skipped every paper; its snapshot holds the outputs of 79bf9038",
}
HEADER = ["session_id", "step", "slug", "date", "git", "claude_md_sha256", "metadata_sha256",
          "paper", "level", "column", "tp", "fp", "fn", "precision", "recall", "f1", "f05",
          "fp_extra", "precision_filled"]
DETAIL_HEADER = ["session_id", "slug", "paper", "taxon", "column", "kind", "model_value", "answer_value", "model_source_location"]

RANK_RE = re.compile(r"\b(subsp|ssp|var|f|forma|nothosubsp)\.?\s+", re.I)


def stem_key(stem):
    return stem.replace(" ", "_")


# file stems before the PDF renaming (1_clean_pdf.py, 2026-10-20) -> current stem, so runs from before the
# renaming score against the same answers; older stems may be longer (matched by their start)
OLD_STEMS = {
    "Kubiak_Cunn_2009": "Kubiak_2009",
    "biostor-259750": "Wark_1997",
    "Post_fire_juvenile_period_of_plants_in_s": "Burrows_et_al_2008",
    "Benson_1985_Cunninghamia": "Benson_1985",
    "Austral_Ecology_-_2025_-_Miller": "Miller_et_al_2025",
    "Austral_Ecology_-_2002_-_Wahren": "Wahren_et_al_2001",
    "AuldScottProcFireEffectsIAWF1997": "Auld_et_al_1995",
    "wf24046": "Enright_et_al_2025",
    "Journal_of_Ecology_-_2002_-_Enright": "Enright_et_al_1998",
    "enright1996": "Enright_et_al_1996",
    "bt9830293": "Pyke_1983",
    "Australian_Journal_of_Ecology_-_December_1988_-_BRADSTOCK": "Bradstock_et_al_1988",
    "BF00040753": "Zammit_et_al_1987",
    "bt9890001": "Ashton_et_al_1989",
    "bt02009": "Denham_et_al_2002",
    "1-s2.0-S0006320798001128-main": "Morgan_et_al_1999",
    "J_Vegetation_Science_-_2007_-_Auld": "Auld_et_al_2007",
    "Knox_&_Clarke_2004": "Knox_et_al_2004",
}


def paper_of_stem(stem):
    """Paper id = the paper's current file stem (results: file_name; answers: stem of Path)."""
    k = stem_key(stem)
    return next((new for old, new in OLD_STEMS.items() if k.startswith(old)), k)


def taxon(genus, species, subsp):
    clean = lambda s: re.sub(r"\s+(s\.\s?lat|s\.\s?str|sens\.\s?lat)\.?$", "", re.sub(r"[?*()\"]", "", s.replace("\u2013", "-").replace("\xa0", " ")).strip().lower())  # noqa: E731
    sub = clean(RANK_RE.sub("", subsp)) if subsp.strip() not in ("*", "NA") else ""
    key = (clean(genus), clean(species), sub)
    printed = clean(subsp) if sub else ""
    PRINTED.setdefault(key, " ".join(x for x in (key[0].capitalize(), key[1], printed) if x))
    return key


PRINTED = {}  # taxon key -> its name as first printed (rank word kept), for --taxa


def load_taxon_map():
    """Taxon key -> key of its APC accepted name (rows with use = yes); other names are left out (kept as printed)."""
    if not TAXON_MAP.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(TAXON_MAP, encoding="utf-8", newline="")):
        accepted = r["accepted_name"].split()
        if r["use"] == "yes" and len(accepted) >= 2:
            out[(r["genus"], r["species"], r["subsp"])] = taxon(accepted[0], accepted[1], " ".join(accepted[2:]))
    return out


def accepted(taxa, taxon_map):
    """Taxa renamed to their accepted names (taxa with the same accepted name merged), and the original keys of each."""
    out = defaultdict(lambda: defaultdict(set))
    orig = defaultdict(set)
    for t, cols in taxa.items():
        a = taxon_map.get(t, t)
        orig[a].add(t)
        for col, values in cols.items():
            out[a][col] |= values
    return out, orig


UNCERTAIN_RE = re.compile(r"\b(?:circa|approx(?:imately)?\.?|ca\.?|c\.)\s*|~|\?", re.I)
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
VALUE_RE = re.compile(r"([<>]?)(-?\d+(?:\.\d+)?)(?:-(\d+(?:\.\d+)?))?")  # bound, number, optional range end
MAX_TOL = 0.05  # numbers may differ by rounding to the coarser printed precision, at most this much
COORD_TOL = 0.01  # decimal degrees


def plain(v):
    """Number text without uncertainty marks (c., ca., approx., ~, ?) and thousands commas; digits as printed."""
    v = UNCERTAIN_RE.sub("", v).strip()
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", v)


def norm(col, value):
    """Normalised values of a cell (a set: one cell can hold several values)."""
    v = value.strip().replace("–", "-").replace("—", "-")
    if not v or v == "NA":
        return set()
    if col in COORDS:
        n = plain(v)
        return {n} if NUMBER_RE.fullmatch(n) else {v.lower()}
    if col in NUMERIC:  # digits kept as printed ('3.0' stays '3.0'): same() reads the precision from them
        v = re.sub(r"\s*-\s*", "-", plain(v))
        if col == "rainfall_mm":  # '698-843' and '698; 843' both = the 2 bounds
            return {n for n in (x.strip() for x in re.split(r"[-;,]", v)) if NUMBER_RE.fullmatch(n)} or {v.lower()}
        return {v} if VALUE_RE.fullmatch(v) else {v.lower()}
    if col == "fire_response_categorical_surv1":
        return {v.lower() if v.lower() in ("obligate", "resprouter") else v.replace(" ", "")}
    parts = [p.strip().lower() for p in re.split(r"[;/,]| and | or ", v) if p.strip()]
    if col == "resprouter_type":
        parts = [re.sub(r"(?<=[a-rt-z])s$", "", p) for p in parts]  # rhizomes -> rhizome
    return {"; ".join(sorted(parts))} if col == "fire_season_categorical" else set(parts)


def to_years(value, factor):
    m = re.fullmatch(r"([<>]?)([\d.]+)(?:-([\d.]+))?", value)
    if not m:
        return value
    conv = lambda s: f"{round(float(s) * factor, 3):g}"  # noqa: E731
    return m.group(1) + conv(m.group(2)) + (f"-{conv(m.group(3))}" if m.group(3) else "")


def load_fire_class():
    """(paper or '*', code) -> fire response class (obligate, O/R or resprouter), from FIRE_PCT."""
    if not FIRE_PCT.exists():
        return {}
    return {(r["paper"], r["code"]): r["class"] for r in csv.DictReader(open(FIRE_PCT, encoding="utf-8", newline=""))}


FIRE_CLASS_MAP = load_fire_class()


def fire_class(paper, code):
    """Class of a fire response code: the paper's own definition first, then the standard class."""
    return FIRE_CLASS_MAP.get((paper, code)) or FIRE_CLASS_MAP.get(("*", code))


def same(col, a, b, paper=None):
    """Values equal: same bound and range form; each number within half a unit of the coarser printed precision,
    at most MAX_TOL ('2' ~ '2.0', '1.6' ~ '1.65', '2' !~ '2.5'); coordinates within COORD_TOL."""
    if a == b:
        return True
    if col == "fire_response_categorical_surv1":  # equal when their classes match ('K' ~ 'obligate', 'FRR' ~ 'O/R')
        ca = fire_class(paper, a)
        return ca is not None and ca == fire_class(paper, b)
    if col not in NUMERIC and col not in COORDS:
        return False
    pa, pb = VALUE_RE.fullmatch(a), VALUE_RE.fullmatch(b)
    if not pa or not pb or pa.group(1) != pb.group(1) or bool(pa.group(3)) != bool(pb.group(3)):
        return False
    for x, y in ((pa.group(2), pb.group(2)), (pa.group(3), pb.group(3))):
        if x is None:
            continue
        d = min(len(x.split(".")[1]) if "." in x else 0, len(y.split(".")[1]) if "." in y else 0)
        tol = COORD_TOL if col in COORDS else min(0.5 * 10 ** -d, MAX_TOL)
        if abs(float(x) - float(y)) > tol + 1e-9:
            return False
    return True


def match(col, av, mv, paper=None):
    """Pair answer and model values; returns (matched, model-only, answer-only)."""
    if col == "fire_response_categorical_surv1":  # codes of one class ('K; pK' ~ 'obligate'): each value may cover several
        a_left = [a for a in sorted(av) if not any(same(col, a, m, paper) for m in mv)]
        m_left = [m for m in sorted(mv) if not any(same(col, a, m, paper) for a in av)]
        return len(av) - len(a_left), m_left, a_left
    a_left, m_left, hits = sorted(av), sorted(mv), 0
    for m in list(m_left):
        hit = next((a for a in a_left if same(col, a, m, paper)), None)
        if hit is not None:
            a_left.remove(hit)
            m_left.remove(m)
            hits += 1
    return hits, m_left, a_left


def typo(a, b):
    """Names differ by a typo: edit distance <= 2 and length difference <= 1 (not 'hispida' vs 'hispidula')."""
    if abs(len(a) - len(b)) > 1:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 2


def scores(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else ""
    r = tp / (tp + fn) if tp + fn else ""
    f = lambda b: (1 + b * b) * p * r / (b * b * p + r) if p != "" and r != "" and (p or r) else ""  # noqa: E731
    return [round(x, 4) if x != "" else "" for x in (p, r, f(1), f(0.5))]


def read_ods(path):
    """Rows of the first sheet of an .ods file as dicts keyed by the header row (stdlib only).
    Number cells give their stored value, not the displayed one, so a cell format cannot truncate decimals."""
    ns = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
          "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
          "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
    q = lambda prefix, name: f"{{{ns[prefix]}}}{name}"  # noqa: E731
    with zipfile.ZipFile(path) as z:
        root = ElementTree.fromstring(z.read("content.xml"))
    sheet = root.find(".//table:table", ns)
    rows = []
    for row in sheet.iter(q("table", "table-row")):
        cells = []
        for c in row:
            if c.tag not in (q("table", "table-cell"), q("table", "covered-table-cell")):
                continue
            if c.get(q("office", "value-type")) in ("float", "percentage", "currency"):
                v = c.get(q("office", "value"), "")
            else:
                v = "\n".join("".join(p.itertext()) for p in c.findall("text:p", ns))
            cells += [v] * int(c.get(q("table", "number-columns-repeated"), "1"))
        if any(v.strip() for v in cells):  # skip blank rows (often repeated thousands of times)
            rows.append(cells)
    header = [h.strip() for h in rows[0]]
    return [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in rows[1:]]


def load_answers():
    rows = [r for path in ANSWERS for r in read_ods(path)]
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))  # paper -> taxon -> column -> values
    no_path = 0
    for r in rows:
        if not r.get("Genus", "").strip():
            continue
        pdf = r.get("Path", "").strip()
        if not pdf:
            no_path += 1
            continue
        if not (REPO / pdf).exists():
            print(f"warning: answer Path not found: {pdf}", file=sys.stderr)
        paper = paper_of_stem(Path(pdf).stem)
        t = taxon(r["Genus"], r["Species"], r.get("subsp", ""))
        cell = out[paper][t]
        cell["_present"].add("1")
        for a, c in VALUE_COLS.items():
            cell[c] |= norm(c, r.get(a, ""))
        if "*" in r.get("subsp", "") + r.get("scientific_name", ""):
            cell["introduced"].add("introduced")
    if no_path:
        print(f"warning: {no_path} answer rows without Path (not scored)", file=sys.stderr)
    return out


def read_result(run_dir, slug):
    """Final result rows of a snapshot, or None. Snapshots from raw extraction on (2026-10-26) hold only
    {slug}_raw.csv; it is normalised here with the same code as scripts/pipeline/5_normalise.py."""
    final, raw = run_dir / f"{slug}.csv", run_dir / f"{slug}_raw.csv"
    if final.exists():
        return list(csv.DictReader(open(final, encoding="utf-8", newline="")))
    if not raw.exists():
        return None
    spec = importlib.util.spec_from_file_location("normalise", REPO / "scripts/pipeline/5_normalise.py")
    normalise = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(normalise)
    problems = []
    rows = csv.DictReader(open(raw, encoding="utf-8", newline=""))
    return [normalise.normalise_row(split_units(r, normalise), problems, f"raw line {i}") for i, r in enumerate(rows, 2)]


def split_units(row, normalise):
    """Raw rows from before the <column>_unit columns (2026-10-30) hold '<value> <unit>' in one cell: split it."""
    for col in normalise.YEARS_COLS + normalise.VARIABLE_COLS + [normalise.PJP]:
        if col + "_unit" in row:
            continue
        if row.get(col, "").strip() == "NA":  # NA row
            row[col + "_unit"] = "NA"
            continue
        m = re.fullmatch(r"(.+?)\s*([A-Za-z]+)\.?", row.get(col, "").strip())
        row[col], row[col + "_unit"] = (m.group(1), m.group(2)) if m else (row.get(col, ""), "")
    row.pop("time_unit", None)
    return row


def load_run(run_dir):
    slug = run_dir.name.split("_")[1]
    session = run_dir.name.split("_", 2)[2]
    result, log = read_result(run_dir, slug), run_dir / f"{slug}_log.csv"
    if result is None or not log.exists():
        return None
    log_rows = list(csv.DictReader(open(log, encoding="utf-8", newline="")))
    runs = [r for r in log_rows if r["paper"] == "_run"]
    if not runs:
        return None
    start = runs[-1]["started"]
    fresh = {stem_key(r["paper"]) for r in log_rows if r["paper"] != "_run" and r["started"] >= start}
    note = runs[-1]["note"]
    meta = run_dir / "metadata.csv"
    info = {
        "session_id": session, "step": "step1", "slug": slug, "date": start[:10],
        "git": (re.search(r"git=([0-9a-f]+)", note) or [None, ""])[1],
        "claude_md_sha256": (re.search(r"claude_md_sha256=([0-9a-f]+)", note) or [None, ""])[1],
        "metadata_sha256": hashlib.sha256(meta.read_bytes()).hexdigest() if meta.exists() else "",
    }
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    where = defaultdict(dict)
    for r in result:
        r = {k.strip(): v for k, v in r.items() if k}
        g = lambda *names: next((r[n] for n in names if n in r), "")  # noqa: E731  old or new column name
        stem = stem_key(g("file_name", "File_name"))
        paper = paper_of_stem(stem)
        if not paper or stem not in fresh or g("genus", "Genus") in ("NA", ""):
            continue
        t = taxon(g("genus", "Genus"), g("species", "Species"), g("subsp"))
        cell = out[paper][t]
        cell["_present"].add("1")
        for a, c in VALUE_COLS.items():
            values = norm(c, g(c, a))
            unit = YEARS_PER.get(g(c + "_unit", "time_unit", "Time_unit").strip().lower(), 1)  # older runs: one time_unit per row
            if c in VARIABLE_UNIT and unit != 1:  # answers are in years
                values = {to_years(v, unit) for v in values}
            cell[c] |= values
        if g("native_status").strip().lower() in INTRODUCED or "*" in g("subsp") + g("scientific_name"):
            cell["introduced"].add("introduced")
        where[paper].setdefault(t, (g("data_location") or g("notes", "Notes").split(";")[0]).strip()[:80])  # older runs: location in notes
    return info, out, where, {paper_of_stem(s) for s in fresh} - {None}


def score_run(info, model, where, papers, answers, taxon_map):
    lines, details = [], []
    totals = defaultdict(lambda: [0, 0, 0, 0])
    cols = list(VALUE_COLS.values()) + ["introduced"]
    for paper in sorted(p for p in papers if p in answers):
        # names to their APC accepted names first (Danthonia pilosa ~ Rytidosperma pilosum)
        ans, a_orig = accepted(answers[paper], taxon_map)
        mod, m_orig = accepted(model.get(paper, {}), taxon_map)
        where[paper] = {taxon_map.get(t, t): v for t, v in where[paper].items()}
        # exact taxon match, then pair the rest by typo (e.g. 'poa sieheriana' ~ 'poa sieberiana')
        pairs = {t: t for t in set(ans) & set(mod)}
        name = lambda t: " ".join(x for x in t if x)  # noqa: E731
        for m in sorted(set(mod) - set(pairs)):
            free = [a for a in set(ans) - set(pairs.values()) if a[0] == m[0]]
            best = max(free, key=lambda a: SequenceMatcher(None, name(a), name(m)).ratio(), default=None)
            if best and typo(name(best), name(m)):
                pairs[m] = best
                details.append([paper, name(m), "taxon", "spelling", name(m), name(best), where[paper].get(m, "")])
        mod = {pairs.get(t, t): v for t, v in mod.items()}  # model taxa renamed to their answer spelling
        m_orig = {pairs.get(t, t): v for t, v in m_orig.items()}
        where[paper] = {pairs.get(t, t): v for t, v in where[paper].items()}
        a_t, m_t = set(ans), set(mod)
        rec = [len(a_t & m_t), len(m_t - a_t), len(a_t - m_t)]
        lines.append([paper, "record", "taxon", *rec])
        for k in range(3):
            totals[("record", "taxon")][k] += rec[k]
        names = lambda keys: "; ".join(sorted(name(k) for k in keys))  # noqa: E731
        for t in sorted(a_t & m_t):
            renamed = any(taxon_map.get(k, k) != k for k in m_orig[t] | a_orig[t])  # typo pairs are logged as 'spelling'
            if renamed and m_orig[t] != a_orig[t]:
                details.append([paper, name(t), "taxon", "synonym", names(m_orig[t]), names(a_orig[t]), where[paper].get(t, "")])
        for t in sorted(m_t - a_t):
            details.append([paper, " ".join(x for x in t if x), "taxon", "extra", "", "", where[paper].get(t, "")])
        for t in sorted(a_t - m_t):
            details.append([paper, " ".join(x for x in t if x), "taxon", "missed", "", "", ""])
        for col in cols:
            c = [0, 0, 0, 0]  # tp, fp, fn, fp_extra
            for t in sorted(a_t & m_t):
                av, mv = ans[t][col], mod[t][col]
                hits, m_only, a_only = match(col, av, mv, paper)
                c[0] += hits
                c[1] += len(m_only)
                c[2] += len(a_only)
                if not av:
                    c[3] += len(m_only)
                if m_only or a_only:
                    kind = "wrong" if av and mv else ("extra" if mv else "missed")
                    details.append([paper, " ".join(x for x in t if x), col, kind,
                                    "; ".join(sorted(mv)), "; ".join(sorted(av)), where[paper].get(t, "")])
            if any(c):
                lines.append([paper, "value", col, *c])
                for key in ((col,), ("_all",)):
                    for k in range(4):
                        totals[("value",) + key][k] += c[k]
    for (level, col), c in totals.items():
        lines.append(["_all", level, col, *c])
    base = [info[k] for k in HEADER[:7]]
    def filled(line):
        if line[1] != "value":
            return ["", ""]
        tp, fp, extra = line[3], line[4], line[6]
        return [extra, round(tp / (tp + fp - extra), 4) if tp + fp - extra else ""]
    rows = [base + line[:6] + scores(*line[3:6]) + filled(line) for line in lines]
    return rows, [[info["session_id"], info["slug"], *d] for d in details]


def write(path, header, rows, drop_sessions):
    old = []
    if path.exists():
        old = [r for r in csv.reader(open(path, encoding="utf-8", newline=""))][1:]
        old = [r for r in old if r[0] not in drop_sessions]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(old + rows)


def latest_by_paper():
    """benchmark.csv lines of the latest scored run of each (slug, paper), latest = start time in sessions.csv."""
    started = {}
    if SESSIONS.exists():
        started = {r["session_id"]: r["date"] for r in csv.DictReader(open(SESSIONS, encoding="utf-8", newline="")) if r["step"] == "step1"}
    lines = [r for r in csv.DictReader(open(OUT, encoding="utf-8", newline="")) if r["paper"] != "_all"]
    best = {}
    for r in lines:
        key = (r["slug"], r["paper"])
        rank = (started.get(r["session_id"], r["date"]), r["session_id"])
        if key not in best or rank > best[key]:
            best[key] = rank
    return [r for r in lines if best[(r["slug"], r["paper"])][1] == r["session_id"]]


def report(show):
    """Per-paper scores from the latest run of each paper (benchmark_papers.csv), and per-column totals with their metric."""
    lines = latest_by_paper()
    head = ["slug", "paper", "session_id", "date", "taxa_tp", "taxa_fp", "taxa_fn", "taxa_precision", "taxa_recall",
            "values_tp", "values_fp", "values_fn", "values_precision", "values_recall", "values_f05", "values_fp_extra", "values_precision_filled"]
    out, col_tot = [], defaultdict(lambda: [0, 0, 0, 0])
    for slug in sorted({r["slug"] for r in lines}):
        tot = {"record": [0, 0, 0, 0], "value": [0, 0, 0, 0]}
        for paper in sorted({r["paper"] for r in lines if r["slug"] == slug}):
            mine = [r for r in lines if r["slug"] == slug and r["paper"] == paper]
            rec = next((r for r in mine if r["level"] == "record"), None)
            val = [r for r in mine if r["level"] == "value"]
            if not rec:
                continue
            c = {"record": [int(rec[k]) for k in ("tp", "fp", "fn")] + [0],
                 "value": [sum(int(r[k] or 0) for r in val) for k in ("tp", "fp", "fn", "fp_extra")]}
            for r in val:
                for k, name in enumerate(("tp", "fp", "fn", "fp_extra")):
                    col_tot[(slug, r["column"])][k] += int(r[name] or 0)
            for level in c:
                tot[level] = [a + b for a, b in zip(tot[level], c[level])]
            out.append([slug, paper, rec["session_id"], rec["date"], *paper_cells(c)])
        out.append([slug, "_all", "", "", *paper_cells(tot)])
    with open(PAPERS_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        w.writerows(out)
    print(f"written: {PAPERS_OUT.relative_to(REPO)} (latest run of each paper per agent)")
    if not show:
        return
    for slug in sorted({r[0] for r in out}):
        print(f"\n{slug}: per paper (latest run of each paper)")
        print(f"  {'paper':22} {'run':8} | {'taxa tp/fp/fn':>14} {'P':>5} {'R':>5} | {'values tp/fp/fn':>15} {'P':>5} {'R':>5} {'F0.5':>5}")
        for r in (r for r in out if r[0] == slug):
            print(f"  {r[1]:22} {r[2][:8]:8} | {f'{r[4]}/{r[5]}/{r[6]}':>14} {fmt(r[7]):>5} {fmt(r[8]):>5} | "
                  f"{f'{r[9]}/{r[10]}/{r[11]}':>15} {fmt(r[12]):>5} {fmt(r[13]):>5} {fmt(r[14]):>5}")
        print(f"\n{slug}: per column (same runs)")
        print(f"  {'column':48} {'tp/fp/fn':>13} {'P':>5} {'R':>5}  metric")
        for col, metric in METRICS.items():
            if col == "taxon":
                t = next(r for r in out if r[0] == slug and r[1] == "_all")
                cells, pr = f"{t[4]}/{t[5]}/{t[6]}", (t[7], t[8])
            elif (slug, col) in col_tot:
                tp, fp, fn, _ = col_tot[(slug, col)]
                cells, pr = f"{tp}/{fp}/{fn}", scores(tp, fp, fn)[:2]
            else:
                continue
            print(f"  {col:48} {cells:>13} {fmt(pr[0]):>5} {fmt(pr[1]):>5}  {metric}")


def paper_cells(c):
    rec, val = c["record"], c["value"]
    p, r = scores(*rec[:3])[:2]
    vp, vr, _, vf = scores(*val[:3])
    filled = round(val[0] / (val[0] + val[1] - val[3]), 4) if val[0] + val[1] - val[3] else ""
    return [*rec[:3], p, r, *val[:3], vp, vr, vf, val[3], filled]


def fmt(x):
    return f"{x:.2f}" if isinstance(x, float) else ("" if x == "" else str(x))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rescore", action="store_true", help="score all snapshots again")
    parser.add_argument("--run", help="score only this snapshot folder (name or path)")
    parser.add_argument("--report", action="store_true", help="print per-paper and per-column scores of the latest run of each paper; no scoring")
    parser.add_argument("--taxa", action="store_true", help="write every taxon name in the answers and the runs to logs/benchmark_taxa.csv, for 6a_taxon_map.R")
    args = parser.parse_args()

    if args.report:
        report(show=True)
        return
    answers = load_answers()
    if args.taxa:  # names of the papers with answers only; other papers are never scored
        keys = {t for taxa in answers.values() for t in taxa}
        for d in sorted(RUNS.glob("step1_*")):
            loaded = load_run(d)
            if loaded:
                keys |= {t for paper, taxa in loaded[1].items() if paper in answers for t in taxa}
        with open(TAXA, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["genus", "species", "subsp", "name"])
            w.writerows([*k, PRINTED[k]] for k in sorted(keys))
        print(f"written: {TAXA.relative_to(REPO)} ({len(keys)} names); next: Rscript scripts/claude/6a_taxon_map.R")
        return
    taxon_map = load_taxon_map()
    print(f"taxon map: {len(taxon_map)} names with an APC accepted name" if taxon_map else
          f"taxon map: none ({TAXON_MAP.relative_to(REPO)} missing); names compared as printed")
    done = set()
    if OUT.exists() and not args.rescore:
        done = {r["session_id"] for r in csv.DictReader(open(OUT, encoding="utf-8", newline=""))}
    dirs = [RUNS / Path(args.run).name] if args.run else sorted(RUNS.glob("step1_*"))
    all_rows, all_details, scored = [], [], set()
    for d in dirs:
        session = d.name.split("_", 2)[2]
        if session in SKIP:
            continue
        if session in done and not args.run:
            continue
        loaded = load_run(d)
        if not loaded:
            continue
        info, model, where, papers = loaded
        rows, details = score_run(info, model, where, papers, answers, taxon_map)
        if not rows:
            print(f"skip {d.name}: no scored papers (none extracted in this run, or none with answers)")
            continue
        all_rows += rows
        all_details += details
        scored.add(session)
        tot = {(r[8], r[9]): r for r in rows if r[7] == "_all"}
        rec, val = tot.get(("record", "taxon")), tot.get(("value", "_all"))
        n = len({r[7] for r in rows} - {"_all"})
        print(f"{info['date']} {info['slug']:10} {session[:8]} | papers {n:2} | taxa P {rec[13]} R {rec[14]} F0.5 {rec[16]}"
              + (f" | values P {val[13]} R {val[14]} F0.5 {val[16]}" if val else ""))
    if scored:
        write(OUT, HEADER, all_rows, scored | set(SKIP))
        write(DETAILS, DETAIL_HEADER, all_details, scored | set(SKIP))
        print(f"written: {OUT.relative_to(REPO)}, {DETAILS.relative_to(REPO)}")
        report(show=False)


if __name__ == "__main__":
    main()
