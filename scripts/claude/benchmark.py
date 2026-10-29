"""Score Step 1 results against the human-extracted answers (accuracy benchmark).

Usage (from the repo root):
    python scripts/claude/benchmark.py              # score every Step 1 snapshot in logs/runs/ not yet in benchmark.csv
    python scripts/claude/benchmark.py --rescore    # score all snapshots again
    python scripts/claude/benchmark.py --run <dir>  # score one snapshot folder

Ground truth: data/papers_test/answers/juvenile_period_data_part*.ods, first sheet of each (agents never read it).
Answer rows are matched to papers by the start of their Source; papers without answer rows are not scored.
Only papers extracted in the run itself are scored (LOG started >= the run's last _run line), so papers
carried over from an earlier run are not counted twice.

Two levels, each with true positives (tp), false positives (fp) and false negatives (fn):
  record: taxa (genus + species + subsp) per paper. tp = taxon in both; fp = model only; fn = answers only.
  value:  for each taxon in both, the set of values of a column over the taxon's rows.
          tp = values in both; fp = model values not in the answers (wrong or extra); fn = answer values the model lacks.
Scores: precision, recall, f1, and f05 (F0.5: precision weighted twice as much as recall; headline score).
  fp_extra: the part of fp where the answer cell is empty (model value unverified: the answers may simply
  not record it); precision_filled = tp / (tp + fp - fp_extra), i.e. precision over cells both sides filled.

Writes, under data/inference_test/logs/:
  benchmark.csv          1 line per run x paper x level x column, plus totals (paper "_all", column "_all");
                         joins sessions.csv on (session_id, step)
  benchmark_details.csv  1 line per taxon or value in only one side, with the model's source location (data_location; notes in older runs)
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

# start of the answer Source -> start of the paper's file stem (spaces as "_")
PAPERS = [
    ("Kubiak PJ. (2009)", "Kubiak_Cunn_2009"),
    ("Wark, M.C. (1997)", "biostor-259750"),
    ("Burrows, N. D., Wardell-Johnson", "Post_fire_juvenile_period_of_plants_in_s"),
    ("Burrows, G.E. (1995)", "Burrows_1995"),
    ("Benson, D. (1985)", "Benson_1985_Cunninghamia"),
    ("Miller, R.G., Enright", "Austral_Ecology_-_2025_-_Miller"),
    ("Muir AM", "Muir_et_al_2014"),
    ("Wahren, C.-H.A.", "Austral_Ecology_-_2002_-_Wahren"),
    ("Auld, T.D. & Scott, J. (1997)", "AuldScottProcFireEffectsIAWF1997"),
    ("Enright N.J. & Agne M.C. (2025)", "wf24046"),
    ("Enright, N.J., Marsula", "Journal_of_Ecology_-_2002_-_Enright"),
    ("Enright, N. J., Lamont, B. B., & Marsula", "enright1996"),
    ("Pyke, G.H. (1983)", "bt9830293"),
    ("Bradstock, R.A. & O'Connell", "Australian_Journal_of_Ecology_-_December_1988_-_BRADSTOCK"),
    ("Zammit & Westoby (1987)", "BF00040753"),
    ("Ashton, D.H. & Chappill", "bt9890001"),
    ("Denham, A.J. & Auld, T.D. (2002)", "bt02009"),
    ("Morgan, J.W & Lunt", "1-s2.0-S0006320798001128-main"),
    ("Auld, Tony D, Andrew J Denham", "J_Vegetation_Science_-_2007_-_Auld"),
    ("Knox K.J.E. & Clarke P.J. (2004)", "Knox_&_Clarke_2004"),
]

# answer column (old name) -> result column (new name); scored at the value level
VALUE_COLS = {
    "PJP mths": "pjp_mths",
    "Time to 50% flowering_repr4": "time_to_50_percent_flowering_repr4",
    "Age at first flower production from seed_repr3": "age_at_first_flower_production_from_seed_repr3",
    "Time to first flower production resprout_repr3a": "time_to_first_flower_production_resprout_repr3a",
    "primary_juvenile_period": "primary_juvenile_period",
    "secondary_juvenile_period": "secondary_juvenile_period",
    "fire_response categorical_surv1": "fire_response_categorical_surv1",
    "resprouter_type": "resprouter_type",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Rainfall_mm": "rainfall_mm",
    "Fire_season_categorical": "fire_season_categorical",
    "Fire_severity_categorical": "fire_severity_categorical",
}
NUMERIC = {"pjp_mths", "time_to_50_percent_flowering_repr4", "age_at_first_flower_production_from_seed_repr3",
           "time_to_first_flower_production_resprout_repr3a", "primary_juvenile_period", "secondary_juvenile_period",
           "rainfall_mm"}
COORDS = {"latitude", "longitude"}
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


def paper_of_source(source):
    s = source.strip()
    return next((p for prefix, p in PAPERS if s.startswith(prefix)), None)


# file stems after the PDF renaming (1_clean_pdf.py, 2026-10-20) -> paper id (old stem) in PAPERS,
# so scores stay comparable with runs before the renaming
RENAMED = {
    "Kubiak_2009": "Kubiak_Cunn_2009",
    "Wark_1997": "biostor-259750",
    "Burrows_et_al_2008": "Post_fire_juvenile_period_of_plants_in_s",
    "Benson_1985": "Benson_1985_Cunninghamia",
    "Miller_et_al_2025": "Austral_Ecology_-_2025_-_Miller",
    "Wahren_et_al_2001": "Austral_Ecology_-_2002_-_Wahren",
    "Auld_et_al_1995": "AuldScottProcFireEffectsIAWF1997",
    "Enright_et_al_2025": "wf24046",
    "Enright_et_al_1998": "Journal_of_Ecology_-_2002_-_Enright",
    "Enright_et_al_1996": "enright1996",
    "Pyke_1983": "bt9830293",
    "Bradstock_et_al_1988": "Australian_Journal_of_Ecology_-_December_1988_-_BRADSTOCK",
    "Zammit_et_al_1987": "BF00040753",
    "Ashton_et_al_1989": "bt9890001",
    "Denham_et_al_2002": "bt02009",
    "Morgan_et_al_1999": "1-s2.0-S0006320798001128-main",
    "Auld_et_al_2007": "J_Vegetation_Science_-_2007_-_Auld",
    "Knox_et_al_2004": "Knox_&_Clarke_2004",
}


def paper_of_stem(stem):
    k = stem_key(stem)
    k = RENAMED.get(k, k)
    return next((p for _, p in PAPERS if k.startswith(p)), None)


def taxon(genus, species, subsp):
    clean = lambda s: re.sub(r"\s+(s\.\s?lat|s\.\s?str|sens\.\s?lat)\.?$", "", re.sub(r"[?*()\"]", "", s.replace("\u2013", "-").replace("\xa0", " ")).strip().lower())  # noqa: E731
    sub = clean(RANK_RE.sub("", subsp)) if subsp.strip() not in ("*", "NA") else ""
    return (clean(genus), clean(species), sub)


def number(s):
    s = s.strip().lstrip("~").replace("c.", "").strip()
    try:
        return f"{float(s):g}"
    except ValueError:
        return None


def norm(col, value):
    """Normalised values of a cell (a set: one cell can hold several values)."""
    v = value.strip().replace("–", "-").replace("—", "-")
    if not v or v == "NA":
        return set()
    if col in COORDS:
        n = number(v)
        return {f"{float(n):.2f}"} if n else {v.lower()}
    if col in NUMERIC:
        v = re.sub(r"\s*-\s*", "-", v)
        if col == "rainfall_mm":  # '698-843' and '698; 843' both = the 2 bounds
            return {n for n in (number(x) for x in re.split(r"[-;,]", v)) if n is not None} or {v.lower()}
        m = re.fullmatch(r"([<>]?)\s*([\d.]+)(?:-([\d.]+))?", v)
        if m:
            lo, hi = number(m.group(2)), number(m.group(3)) if m.group(3) else None
            if lo is not None:
                return {m.group(1) + lo + (f"-{hi}" if hi else "")}
        return {v.lower()}
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


def same(col, a, b):
    """Values equal, allowing rounding: compare at the coarser of the 2 printed precisions (coordinates: 0.01)."""
    if a == b:
        return True
    if col not in NUMERIC and col not in COORDS:
        return False
    pa = re.fullmatch(r"([<>]?)([\d.-]+?)(?:-([\d.]+))?", a)
    pb = re.fullmatch(r"([<>]?)([\d.-]+?)(?:-([\d.]+))?", b)
    if not pa or not pb or pa.group(1) != pb.group(1) or bool(pa.group(3)) != bool(pb.group(3)):
        return False
    for x, y in ((pa.group(2), pb.group(2)), (pa.group(3), pb.group(3))):
        if x is None:
            continue
        try:
            fx, fy = float(x), float(y)
        except ValueError:
            return False
        d = min(len(x.split(".")[1]) if "." in x else 0, len(y.split(".")[1]) if "." in y else 0)
        tol = 0.0051 if col in COORDS else 0.5 * 10 ** -d + 1e-9
        if abs(fx - fy) > tol:
            return False
    return True


def match(col, av, mv):
    """Pair answer and model values; returns (matched, model-only, answer-only)."""
    a_left, m_left, hits = sorted(av), sorted(mv), 0
    for m in list(m_left):
        hit = next((a for a in a_left if same(col, a, m)), None)
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
    for r in rows:
        paper = paper_of_source(r.get("Source", ""))
        if not paper or not r.get("Genus", "").strip():
            continue
        t = taxon(r["Genus"], r["Species"], r.get("subsp", ""))
        cell = out[paper][t]
        cell["_present"].add("1")
        for a, c in VALUE_COLS.items():
            cell[c] |= norm(c, r.get(a, ""))
        if "*" in r.get("subsp", "") + r.get("scientific_name", ""):
            cell["introduced"].add("introduced")
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
    return [normalise.normalise_row(r, problems, f"raw line {i}") for i, r in enumerate(rows, 2)]


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
        unit = YEARS_PER.get(g("time_unit", "Time_unit").strip().lower(), 1)
        for a, c in VALUE_COLS.items():
            values = norm(c, g(c, a))
            if c == "secondary_juvenile_period" and unit != 1:  # answers are in years
                values = {to_years(v, unit) for v in values}
            cell[c] |= values
        if g("native_status").strip().lower() in INTRODUCED or "*" in g("subsp") + g("scientific_name"):
            cell["introduced"].add("introduced")
        where[paper].setdefault(t, (g("data_location") or g("notes", "Notes").split(";")[0]).strip()[:80])  # older runs: location in notes
    return info, out, where, {paper_of_stem(s) for s in fresh} - {None}


def score_run(info, model, where, papers, answers):
    lines, details = [], []
    totals = defaultdict(lambda: [0, 0, 0, 0])
    cols = list(VALUE_COLS.values()) + ["introduced"]
    for paper in sorted(p for p in papers if p in answers):
        ans, mod = answers[paper], model.get(paper, {})
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
        where[paper] = {pairs.get(t, t): v for t, v in where[paper].items()}
        a_t, m_t = set(ans), set(mod)
        rec = [len(a_t & m_t), len(m_t - a_t), len(a_t - m_t)]
        lines.append([paper, "record", "taxon", *rec])
        for k in range(3):
            totals[("record", "taxon")][k] += rec[k]
        for t in sorted(m_t - a_t):
            details.append([paper, " ".join(x for x in t if x), "taxon", "extra", "", "", where[paper].get(t, "")])
        for t in sorted(a_t - m_t):
            details.append([paper, " ".join(x for x in t if x), "taxon", "missed", "", "", ""])
        for col in cols:
            c = [0, 0, 0, 0]  # tp, fp, fn, fp_extra
            for t in sorted(a_t & m_t):
                av, mv = ans[t][col], mod[t][col]
                hits, m_only, a_only = match(col, av, mv)
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


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rescore", action="store_true", help="score all snapshots again")
    parser.add_argument("--run", help="score only this snapshot folder (name or path)")
    args = parser.parse_args()

    answers = load_answers()
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
        rows, details = score_run(info, model, where, papers, answers)
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


if __name__ == "__main__":
    main()
