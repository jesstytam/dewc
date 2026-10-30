# Building an LLM extraction pipeline for a meta-analysis

This file is self-contained. Give it to a Claude Code session in an empty folder, with 1 example of a paper already extracted by hand. The session builds a full extraction pipeline for that study: `CLAUDE.md`, a column dictionary and scripts. It needs no other repository.

## How to run

```bash
mkdir new_study && cd new_study
cp /path/to/ADAPTING_CLAUDE_MD.md /path/to/example.csv /path/to/example.pdf .
claude "Follow ADAPTING_CLAUDE_MD.md. Example extraction: example.csv. Example paper: example.pdf."
```

Inputs:

| File | Required | Content |
|---|---|---|
| `example.csv` | yes | All rows of 1 paper, extracted by hand, with the columns the study needs. Use real column names and the value format wanted in the final data. |
| `example.pdf` | strongly recommended | The paper behind `example.csv`. Without it, the session cannot test rules or trace values to the text. |
| Other pilot PDFs | no | 4 to 19 more papers covering hard cases: long tables, scans, several groups, unusual units, no usable data. Put them in `papers/pdf/` after setup. |

Choose an example paper that shows the hard cases. A paper with 2 rows and no units teaches the session little. If 1 paper cannot show every column, add rows from other papers and say so.

## Instructions for the session

Everything below is addressed to the session building the pipeline.

```python
inputs = read(example_csv, example_pdf)           # Phase 1; stop if example_csv is missing
draft  = infer_design(inputs)                     # Phase 1
answers = ask_study_lead(gaps(draft))             # Phase 2; stop until each gap has an answer
metadata = build_metadata(draft, answers)         # Phase 3
while not approved_by(study_lead, metadata):      # never write CLAUDE.md before this passes
    metadata = revise(metadata)
write_claude_md(TEMPLATE, answers, metadata)      # Phase 4
write_scripts(metadata)                           # Phase 5
test_scripts(example_csv, synthetic_rows)         # Phase 5
pilot()                                           # Phase 6
report_to_study_lead()                            # full run only when the study lead says so
```

Constraints:
- `example.csv` is the only source of truth for the output format. If it conflicts with an answer from the study lead, ask.
- Never fill design decisions from background knowledge of the field. Ask.
- Keep the wording of generic template sections unless a rule fails in the pilot.
- Change one rule at a time between pilot rounds, so a change in score can be traced to it.

### Phase 1: Read the example and infer the design

Read `example.csv` and all of `example.pdf`. Then find each row's values in the paper. Write `design_notes.md` with:

1. **Row unit.** Which columns together make a row unique? E.g. species × site × fire, or study × arm × timepoint × outcome.
2. **Column table.** For each column: type, unit, observed value format, whether it is printed in the paper, carried from elsewhere in the paper (methods, site description), computed or standardised by the extractor.
3. **Context columns.** Values printed once and repeated on many rows.
4. **Transformations.** Every difference between the paper's printed value and the CSV cell: unit conversions, rounding, recoded categories, case changes. Each one becomes a `NORMALISE` step or a `VALUE_MAP` entry, never an agent task.
5. **Row validity.** The minimum content of a row, inferred from the example.
6. **Values not in the paper.** Cells you cannot find. Mark them for Phase 2. Do not guess their source.
7. **Missing columns.** Columns the pipeline needs that the CSV lacks: `data_location`, `data_quote`, `supplementary_material`, `notes`, `source`, `file_name`, `pdf_path`. Add them.

### Phase 2: Ask the study lead

Ask only what Phase 1 could not settle. Ask in one message, grouped, stating your inference for each so the lead can confirm it. Always cover:

- Research question, and the analysis that will use the data.
- Number of papers, and whether any are scans.
- For each column: the definition of the measure, in terms of what was measured, not what it is called.
- Near-matches: similar measures defined differently. Do they go to `notes` only?
- Allowed values of each categorical column, and how paper terms map to them.
- Whether a row-specific value replaces a paper-wide value.
- Which estimate wins if a paper reports several for one measure.
- Required effect sizes, errors and sample sizes, and accepted error types.
- Which values, if any, appear only in figures, and whether to extract them.
- Is there an existing hand-coded dataset for more papers? If not, the pilot key is `example.csv` plus what the lead codes.
- Which models to compare. Default: 2 models.
- Who checks results at the end. Human checking is expected, and it decides how far to push the benchmark.

### Phase 3: Build `references/metadata.csv`

The column dictionary and the only format reference. 1 row per result column, in result order. ` | ` separates alternatives.

```csv
column,group,type,unit,allowed_values,code,definition,rule,example
followup,time,numerical,followup_unit (final: years),,,Time from treatment to last assessment.,"Raw: value as printed; its unit in followup_unit. NORMALISE converts.",12
followup_unit,time,categorical,,days | weeks | months | years,,Unit of followup.,"Fill only with followup: the unit the paper prints, spelled out.",months
```

The 2 rows are an invented example. `code` holds any standard or trait code; leave it empty if there is none.

Design rules:
- **Separate raw from final.** Agents copy values as printed, into `results/{slug}_raw.csv`. `NORMALISE` does all conversion, case and dashes. Agents never do arithmetic.
- **Give each measure printed in mixed units a unit column** (`<col>_unit`). One shared unit column fails, because columns in one row can differ.
- **Choose columns by definition, not by name.** Papers use one term for different measures. Put this in the column's rule, with an example.
- **Say where rejected values go.** Near-matches go to `notes` with their definition. Otherwise agents force them into columns or lose them.
- **Mark columns agents leave empty,** because `NORMALISE` fills them.
- **Examples use the exact form the agent writes.**

Write `references/value_map.csv` if papers use varied terms for one category: paper term, standard value, notes entry to write. Use only definitions the paper prints. An undefined code is copied as printed, never translated.

Show the lead `metadata.csv` and `value_map.csv`, and get approval before Phase 4.

### Phase 4: Write `CLAUDE.md`

Copy the template below. Replace each `{PLACEHOLDER}`. Write the study-specific rules from `design_notes.md`, the answers and `metadata.csv`.

Rule-writing standards:
- One instruction, one concrete example, copied from `example.pdf` if possible.
- State the action. Give the reason only if it decides edge cases.
- Cover conflicts: one value printed for several groups, several estimates of one measure, one value under 2 terms.
- Say what happens to each rejected value.
- Use the terms the papers use.

Template:

````markdown
# Data extraction pipeline

## Setup

```python
AGENTS   = {AGENTS_DICT}                         # slug: exact model ID; one session per agent
slug     = AGENTS key whose model ID is the model running this session   # not in AGENTS: stop and tell the user
MD_AGENT = {FIRST_SLUG}                          # only this agent runs Step 0
METADATA = "references/metadata.csv"             # column dictionary; the only format reference
VALUE_MAP = "references/value_map.csv"           # paper terms -> standard values
MD_RAW   = "papers/md_raw/*.md"                  # pdf2md.py output; last line "<!-- pdf2md: scanned -->" or "<!-- pdf2md: text-layer -->"
PDF      = "papers/pdf/{stem}.pdf"               # source PDF; same stem as its markdown
PAPERS   = "papers/md_llm/*.md"                  # extraction input; pages split by <!-- PAGE BREAK -->
RESULT   = "results/{slug}_raw.csv"              # raw extraction, values as printed; header = COLUMNS, in order
LOG      = "logs/{slug}_log.csv"                 # header: paper,status,n_rows,started,finished,note
MD_LOG   = "logs/md_opt_log.csv"                 # header: paper,status,pdf_pages,n_tables,n_fixes,unresolved,started,finished,note
CHECK    = "scripts/check.py"                    # fixed check script; run it, never edit it
NORMALISE = "scripts/normalise.py"               # RESULT -> final results/{slug}.csv; run by the user, never by agents
```

## Read and write scope

| Step | Read | Write |
|---|---|---|
| 0 | `MD_RAW`, `PDF` | `papers/md_llm/`; move or remove files in `papers/md_raw/`; `MD_LOG`; `CHECK --step0` report |
| 1 | `METADATA`, `VALUE_MAP`, `PAPERS`, `RESULT`, `LOG` | `RESULT`, `LOG`; `CHECK` report |

Everything else is off limits. One-off shell or Python commands are allowed; a code file may be written only to the session scratchpad.

## Steps

`print(...)` = write that status line to the chat. `now_utc()` = output of `date -u +%FT%TZ`.

```python
# Step 0: optimise markdown. Only in a session where slug == MD_AGENT.
for md in sorted(MD_RAW):
    out = "papers/md_llm/" + stem(md) + ".md"
    if exists(out) and out ends with "<!-- md_opt:": remove(md); continue       # finished earlier
    if exists(out): overwrite(out, "")                                          # interrupted: restart
    started = now_utc()
    if md ends with "<!-- pdf2md: text-layer -->":
        move(md, out); replace last line with "<!-- md_opt: none -->"; log_md(stem(md), "text_layer", ...); continue
    if not exists(PDF(stem(md))):
        move(md, out); replace last line with "<!-- md_opt: note=no matching PDF -->"; log_md(stem(md), "no_pdf", ...); continue
    for batch in pages(pdf, max_pages=10):       # read PDF pages as images; never load a long PDF at once
        append(out, optimise(text_for(batch), batch))    # see Markdown optimisation
    append(out, "<!-- md_opt: model=...; date=...; fixes=...; unresolved=... -->")
    log_md(stem(md), "done", ...); remove(md)
run(f"python {CHECK} --step0")

# Step 1: extract. One session per agent. Agents work independently.
if MD_RAW is not empty: stop; tell the user to run Step 0 first
if not exists(RESULT): write headers of RESULT and LOG
log("_run", "start", 0, now_utc(), "", f"model={AGENTS[slug]}; date=...")     # first, before any paper
read(METADATA); read(VALUE_MAP)
for paper in sorted(PAPERS):                     # finish its LOG line before the next paper
    if paper in LOG: continue
    started = now_utc()
    remove rows of paper from RESULT             # leftovers from an interrupted run
    if broken(paper):
        append(RESULT, na_row(paper, reason)); log(paper, "broken", 1, started, now_utc(), reason); check_paper(paper); continue
    for batch in pages(paper, max_pages=10):     # never load a whole long paper at once
        append(RESULT, extract(batch))           # write after every batch
    if n_rows == 0:
        append(RESULT, na_row(paper, reason)); log(paper, "no_data", 1, started, now_utc(), reason); check_paper(paper); continue
    log(paper, "done", n_rows, started, now_utc(), problems)
    check_paper(paper)
run(f"python {CHECK} {slug}")
```

## Markdown optimisation

Compare each scanned paper's raw markdown with its PDF page by page. Fix the markdown so it matches the PDF. Raw text may be poor OCR or empty: then build each page from the page image.

- Tables: rebuild every table as a markdown pipe table, one record per row, values in the correct column. Read tables from the PDF page, not from the broken markdown.
- Text: fix split ligatures, OCR errors, joined words and scrambled word order.
- Remove conversion junk. Put exactly one `<!-- PAGE BREAK -->` between PDF pages.
- Keep all content. Do not summarise, reorder or add text.
- Unreadable value: keep it as printed; list it under `unresolved`.

## Extraction rules

- {ROW_RULE, e.g. One row per species × site × fire.}
- Use only text in the paper. No background knowledge. No estimates.
- Value not stated in paper: leave cell empty.
- Tables often span many pages. Read every page; extract every row.
- Table continues into the next batch: reuse its column headers.
- Carry context values ({CONTEXT_COLUMNS}) from the paper's methods onto every row. Several groups: match each row to its own. Value printed for the row itself: use it instead of the paper-wide value; the paper-wide value in `notes`.
- {ROW_VALIDITY_RULE, e.g. A row needs at least 1 value in {KEY_COLUMNS}.} Values kept only in `notes` never create a row.
- Never merge rows. Same entity printed as 2 separate entries: 1 row per entry. Duplicates are fine.
- Fill a column only when the paper's measure matches the column definition. Choose by definition, not name. Near-matches go in `notes` only, with their definition.
- One value never fills 2 columns.
- Ambiguous measure (paper does not say which it is): `notes` only.
- Codes and units: use only definitions printed in the paper. Undefined code: copy as printed. Unit not stated: leave the value empty; value and "unit not stated" in `notes`.
- Value with uncertainty marks (`c.`, `?`, `approx.`): fill the number; marks in `notes`.
- Several estimates of one measure: {ESTIMATE_RULE}; the others in `notes`.
- Tables may be parsed with one-off code. Then print 3 random parsed rows next to their source lines and confirm they match.
- Every place in `data_location` gets its verbatim quote in `data_quote`, copied from the markdown. `CHECK` searches the paper for it.
- {STUDY_SPECIFIC_RULES}

## Broken papers and papers without data

Every paper gets at least 1 row in `RESULT`. Write an NA row when:
- **broken**: file empty or under 1,000 bytes; no `<!-- md_opt:` end comment; text garbled; read error.
- **no_data**: all pages read, no relevant values found.

```python
na_row = {name: "NA" for name in COLUMNS}        # exactly 1 NA row per paper
na_row["notes"] = reason
na_row["source"] = citation if readable else stem(paper)
na_row["file_name"] = stem(paper)
na_row["supplementary_material"] = items if any else "NA"
```

## Columns

Order in `RESULT`. Each column's definition, unit, allowed values and rule are in `METADATA`.

```python
COLUMNS = {COLUMNS_LIST}
```

{MEASURE_RULES, e.g. Each time column has a unit column after it. Value cell as printed; never convert or round.}

CSV format: UTF-8, comma separator, LF line endings, decimal point `.`. Quote any cell containing a comma, quote or newline. Empty cell = no value; `NA` only in NA rows. Trim spaces. Several values in one cell: separate with `; `. Case and dashes: copy as printed; `NORMALISE` sets them. Uncertain value: keep the format; explain in `notes`.

## Checks

```python
def check_paper(paper):                          # after every paper's LOG line; never skip
    for attempt in 1..3:
        if run(f"python {CHECK} {slug} --paper '{stem(paper)}'") == 0: return
        fix each failed row from the paper; fix LOG n_rows if rows changed
    log the remaining errors in the paper's LOG note
```

After all papers: run `CHECK` without `--paper`, fix errors the same way. Warnings: look, fix if real. Never delete a row silently.

## Do not

- Read `answers/` or `logs/benchmark*.csv`, or another agent's `RESULT` or `LOG`.
- Edit `METADATA`, `VALUE_MAP`, `CHECK` or `NORMALISE`, or anything in `papers/pdf/`.
- Run `NORMALISE` or write the final `results/{slug}.csv`.
- Write any script file outside the session scratchpad.
````

Remove any section the study does not need. When a section is unused, delete its references too.

### Phase 5: Write the scripts

Create this layout:

```text
ADAPTING_CLAUDE_MD.md
CLAUDE.md
design_notes.md
requirements.txt
answers/example.csv            # move example.csv here; agents never read answers/
papers/pdf/  papers/md_raw/  papers/md_llm/
references/metadata.csv  references/value_map.csv
results/  logs/  logs/runs/
scripts/pdf2md.py  scripts/check.py  scripts/normalise.py  scripts/benchmark.py
```

Write:

| Script | Must do |
|---|---|
| `scripts/pdf2md.py` | Convert each `papers/pdf/*.pdf` to `papers/md_raw/{stem}.md`, skipping files already converted. Use `marker_single` from `marker-pdf`, or another converter if it cannot be installed. A paper is scanned if most checked pages are a full-page image, even with an OCR layer. End each file with `<!-- pdf2md: scanned -->` or `<!-- pdf2md: text-layer -->`. |
| `scripts/check.py` | Build row checks from `metadata.csv`: header and order, allowed values, numeric format, value-unit pairing, empty-column rules, NA rows. Check `data_quote` appears in the paper. Check that every markdown file has exactly 1 LOG line, every LOG paper has at least 1 row, `n_rows` matches, and every PDF has a markdown file. Modes: `<slug>`, `<slug> --paper <stem>`, `<slug> --final`, `--step0`. Print a summary, write `logs/{slug}_check.csv`, exit 1 on any error. Never edit results. |
| `scripts/normalise.py` | Read `results/{slug}_raw.csv`, write `results/{slug}.csv`. Apply every transformation from Phase 1. Record each conversion at the start of `notes`. Keep every row. Never edit the raw file. |
| `scripts/benchmark.py` | Compare the final results with `answers/`, matching rows on the row unit. Report precision and recall at row level and value level, with F0.5 as the headline, per paper and overall. Numeric tolerance: half a unit of the coarser precision. Write `logs/benchmark.csv` and `logs/benchmark_details.csv`, with each extra, missed and wrong value. Pool values per row key if the key is coded at a coarser level than the extraction. |

Test before the pilot:
- `check.py` passes `example.csv` once converted to raw form, and fails on deliberately broken rows.
- `normalise.py` turns raw `example.csv` rows back into the original `example.csv` values.
- `benchmark.py` scores `example.csv` against itself at 1.0.
- Synthetic rows: empty cells, NA rows, each unit.

### Phase 6: Pilot

The study lead runs the extraction sessions. Tell them exactly what to run, and rescore when they report back.

```bash
python scripts/pdf2md.py
claude --model <model>   # fresh session per model; prompt: "Run Step 0" (MD_AGENT only), then "Run Step 1"
python scripts/normalise.py <slug> <slug>
python scripts/check.py <slug> --final
python scripts/benchmark.py
```

```python
while scores_or_disagreements_changed:
    run_extraction_per_model()                   # fresh sessions; agents never see answers/ or each other's output
    snapshot("logs/runs/" + run_id, RESULT, LOG, "CLAUDE.md", METADATA, VALUE_MAP)
    for d in disagreements(between_models + against_key):
        cause = classify(d)
        if cause == "rule gap":         fix_rule(d); add_example(d)   # agents read the rule differently
        if cause == "key error":        fix_key(d) or accept(d)       # accept if small and comparisons stay undistorted
        if cause == "scoring artefact": fix_benchmark(d) or note(d)   # correct value scored wrong
        if cause == "agent slip":       pass                          # rule covers it; watch the next round
    move old results aside               # rename with a suffix, so the next run starts clean
```

Read disagreements between models first. If 2 models differ, the rule is usually ambiguous. If 2 models agree against the key, suspect the key or the scoring. A key error needs the lead's decision.

Stop when remaining errors are ones the human check can catch cheaply. A perfect score is not the goal.

### Full run

Only when the study lead says so:

```python
assert {stem(p) for p in papers_pdf} == {stem(p) for p in papers_md}   # a PDF with no markdown gets no row
run_step0(); run_step1_per_model(); normalise(); check_final()
human_check(results)                             # data_location and data_quote find each value fast
```

## Limits

- 1 example paper shows the format, not every edge case. Expect several pilot rounds; rules come mostly from disagreements.
- Accuracy needs its own key. `example.csv` alone cannot measure it; more hand-coded papers give a better estimate.
- Definitions need a domain expert. The session cannot decide what the study should measure.
- Text and tables suit this method. Values only in figures need a separate check.
