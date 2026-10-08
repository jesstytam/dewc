"""Compare the A/B test (Step 1 on raw markdown) with Step 1 on cleaned markdown (see AB.md).

Usage (from the repo root):
    python tests/ab_raw_md/compare.py

Rows are matched by taxon (scientific_name + subsp) within each paper. For each taxon found in
both runs, a column agrees when the set of its values over the taxon's rows is the same in both.

Two comparisons:
  test:  raw markdown (tests/ab_raw_md/results) vs cleaned markdown (Sonnet run e22fd76a), the 14 test papers
  noise: 2 Sonnet runs on the same cleaned markdown and CLAUDE.md (09907120 vs e22fd76a), the 6 earlier
         papers; differences here are run-to-run noise, not caused by the markdown

Writes logs/compare_summary.csv (1 line per comparison and paper) and logs/compare_details.csv
(1 line per taxon and column that differs, and per taxon found in only 1 run).
"""

import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RUNS = REPO / "data/inference_test/logs/runs"
SLUG = "sonnet-5-5"
BASE = RUNS / f"step1_{SLUG}_e22fd76a-04d4-41fa-bf12-fc718952c66e"
NOISE = RUNS / f"step1_{SLUG}_09907120-2b79-4141-933d-7796f325ad25"
TEST = HERE / "results" / f"{SLUG}.csv"
TEST_LOG = HERE / "logs" / f"{SLUG}_log.csv"

COMPARE_COLS = [
    "Family", "native_status",
    "fire_response categorical_surv1", "resprouter_type",
    "PJP mths", "primary_juvenile_period", "Age at first flower production from seed_repr3",
    "secondary_juvenile_period", "Time to first flower production resprout_repr3a",
    "Time to 50% flowering_repr4", "Time to 50% flowering", "Time to 80% flowering",
    "Recovery_time", "Time_unit",
    "Location_name", "Latitude", "Longitude", "Rainfall_mm",
    "Fire_type", "Fire_season_categorical", "Fire_severity_categorical",
]
TIME_COLS = COMPARE_COLS[4:13]


def read_rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8", newline="")))


def by_paper(rows):
    out = defaultdict(list)
    for r in rows:
        out[r["File_name"]].append(r)
    return out


def taxa(rows):
    """taxon -> rows; NA rows are left out."""
    out = defaultdict(list)
    for r in rows:
        if r["Genus"] != "NA":
            out[(r["scientific_name"], r["subsp"])].append(r)
    return out


def values(rows, col):
    return frozenset(r[col] for r in rows if r[col])


def tokens(log_path):
    if not log_path.exists():
        return {}
    return {r["paper"]: r.get("total_tokens", "") for r in read_rows(log_path)}


def compare(name, a_rows, b_rows, papers, a_tokens, b_tokens, summary, details):
    """a = run under test, b = reference run."""
    a_by, b_by = by_paper(a_rows), by_paper(b_rows)
    totals = defaultdict(int)
    print(f"\n== {name}: a = {len(papers)} papers")
    print(f"{'paper':34} {'rows a/b':>11} {'taxa a/b/both':>14} {'fire_resp':>9} {'times':>7} {'site':>7} {'tokens a/b (M)':>15}")
    for paper in papers:
        ta, tb = taxa(a_by[paper]), taxa(b_by[paper])
        both = sorted(set(ta) & set(tb))
        for side, only in (("a only", set(ta) - set(tb)), ("b only", set(tb) - set(ta))):
            for t in sorted(only):
                details.append([name, paper, " ".join(x for x in t if x), side, "", ""])
        agree = defaultdict(int)
        for t in both:
            for col in COMPARE_COLS:
                va, vb = values(ta[t], col), values(tb[t], col)
                if va == vb:
                    agree[col] += 1
                else:
                    details.append([name, paper, " ".join(x for x in t if x), col, "; ".join(sorted(va)), "; ".join(sorted(vb))])
        n = len(both)
        times = sum(agree[c] for c in TIME_COLS) / (n * len(TIME_COLS)) if n else None
        site = sum(agree[c] for c in ("Location_name", "Latitude", "Longitude")) / (n * 3) if n else None
        fire = agree["fire_response categorical_surv1"] / n if n else None
        row = {
            "comparison": name, "paper": paper,
            "rows_a": len(a_by[paper]), "rows_b": len(b_by[paper]),
            "taxa_a": len(ta), "taxa_b": len(tb), "taxa_both": n,
            "fire_response_agree": "" if fire is None else round(fire, 3),
            "times_agree": "" if times is None else round(times, 3),
            "site_agree": "" if site is None else round(site, 3),
            "tokens_a": a_tokens.get(paper, ""), "tokens_b": b_tokens.get(paper, ""),
        }
        summary.append(row)
        for k in ("rows_a", "rows_b", "taxa_a", "taxa_b", "taxa_both"):
            totals[k] += row[k]
        for col in COMPARE_COLS:
            totals["agree_" + col] += agree[col]
        pct = lambda x: "-" if x is None else f"{x:.0%}"  # noqa: E731
        tok = lambda v: f"{int(v) / 1e6:.2f}" if v else "-"  # noqa: E731
        print(f"{paper[:34]:34} {row['rows_a']:>5}/{row['rows_b']:<5} {len(ta):>4}/{len(tb)}/{n:<4} {pct(fire):>9} {pct(times):>7} {pct(site):>7} {tok(row['tokens_a']):>7}/{tok(row['tokens_b'])}")
    n = totals["taxa_both"]
    print(f"{'TOTAL':34} {totals['rows_a']:>5}/{totals['rows_b']:<5} {totals['taxa_a']:>4}/{totals['taxa_b']}/{n}")
    if n:
        print("agreement per column over taxa in both runs:")
        for col in COMPARE_COLS:
            print(f"    {col:48} {totals['agree_' + col] / n:.0%}")


def main():
    summary, details = [], []
    base_rows = read_rows(BASE / f"{SLUG}.csv")
    base_tokens = tokens(BASE / f"{SLUG}_log.csv")

    if TEST.exists():
        test_rows = read_rows(TEST)
        papers = sorted(p.stem for p in (HERE / "papers").glob("*.md"))
        compare("test", test_rows, base_rows, papers, tokens(TEST_LOG), base_tokens, summary, details)
    else:
        print(f"no test result yet: {TEST.relative_to(REPO)}")

    noise_rows = read_rows(NOISE / f"{SLUG}.csv")
    papers = sorted(set(by_paper(noise_rows)))
    compare("noise", noise_rows, base_rows, papers, tokens(NOISE / f"{SLUG}_log.csv"), base_tokens, summary, details)

    out = HERE / "logs"
    with open(out / "compare_summary.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(summary)
    with open(out / "compare_details.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["comparison", "paper", "taxon", "column", "value_a", "value_b"])
        w.writerows(details)
    print(f"\nwritten: {(out / 'compare_summary.csv').relative_to(REPO)}, {(out / 'compare_details.csv').relative_to(REPO)}")


if __name__ == "__main__":
    main()
