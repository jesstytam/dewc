# Data extraction pipeline

## Setup

```python
AGENTS   = {"opus-5-5": "claude-opus-5-5", "sonnet-5-5": "claude-sonnet-5-5"}   # slug: exact model ID; one session per agent
slug     = AGENTS key whose model ID is the model running this session   # not in AGENTS: stop and tell the user
MD_AGENT = "opus-5-5"                            # only this agent runs Step 0
RUN      = "test"                                # "test" = trial run; "full" = final run; keep "test" until the user says otherwise
ROOT     = {"test": "data/inference_test/", "full": "data/inference/"}[RUN]   # read references and write results only under ROOT
TEMPLATE = ROOT + "references/template.csv"      # row 1 = header (29 columns); rows 2+ = worked examples; new columns = NA in examples
METADATA = ROOT + "references/metadata.csv"      # column dictionary: 1 row per RESULT column; type, unit, allowed values, trait code, definition, rule, example
MD_RAW   = "data/papers_test/md/*.md"            # pdf2md.py output
PDF_DONE = "data/papers_test/pdf_done/*.pdf"     # source PDF for each MD_RAW file; same file stem
MD_OPT   = "data/papers_test/md_agents/{stem}.md" # Step 0 output; one file per paper
PAPERS   = "data/papers_test/md_agents/*.md"     # extraction input = MD_OPT; pages split by <!-- PAGE BREAK -->
RESULT   = ROOT + "results/{slug}.csv"           # header = COLUMNS names, in COLUMNS order (28 columns)
LOG      = ROOT + "logs/{slug}_log.csv"          # Step 1 log; header: paper,status,n_rows,started,finished,note + TOKEN_COLS
MD_LOG   = ROOT + "logs/md_opt_log.csv"          # Step 0 log; header: paper,status,pdf_pages,n_tables,n_fixes,unresolved,started,finished,note + TOKEN_COLS
TOKEN_COLS = "n_requests,input_tokens,cache_creation_input_tokens,cache_read_input_tokens,output_tokens,total_tokens"   # last 6 log columns; agents leave them empty, USAGE fills them
USAGE    = "scripts/claude/usage.py"             # token usage per paper; run by the user after each session, never by agents
CHECK    = "scripts/claude/check.py"             # fixed check script; run it, never edit it; writes reports to ROOT + "logs/"
```

## Read and write scope

| Step | Read | Write |
|---|---|---|
| 0 | `MD_RAW`, `PDF_DONE` | `.md` files in `data/papers_test/md_agents/`; `MD_LOG`; `CHECK --step0` report |
| 1 | `METADATA`, `TEMPLATE`, `PAPERS` | `RESULT`, `LOG`; `CHECK` report |

Everything not listed for a step is off limits for that step. One-off shell or Python commands are allowed; a code file may be written only to the session scratchpad (never to the repo), so its full text stays in the session transcript.

## Steps

`print(...)` = write that status line to the chat as plain text, so the user can follow progress. `now_utc()` = output of `date -u +%FT%TZ`, e.g. `2026-10-02T08:04:26Z`. `bar(i, n)` = text progress bar, 20 characters wide: `[######--------------] 2/6 (33%)`.

```python
# Step 0: optimise markdown. Only in a session where slug == MD_AGENT; other sessions never run Step 0.
print(f"Step 0: optimise markdown | {len(MD_RAW)} papers")
if not exists(MD_LOG): write(MD_LOG, "paper,status,pdf_pages,n_tables,n_fixes,unresolved,started,finished,note," + TOKEN_COLS)
for i, md in enumerate(sorted(MD_RAW), 1):
    out = MD_OPT(stem(md))
    if exists(out) and out ends with "<!-- md_opt:":    # finished earlier; resume safe
        print(f"{bar(i, len(MD_RAW))} {stem(md)} | skipped: already done"); continue
    if exists(out): overwrite(out, "")           # unfinished file from an interrupted run: restart from page 1; status "restarted" in note
    started = now_utc()
    pdf = PDF_DONE matching stem(md)
    if not pdf:                                  # copy md unchanged, add end comment with note
        copy(md, out); append(out, "<!-- md_opt: ...; note=no matching PDF -->"); log_md(stem(md), "no_pdf", started=started, finished=now_utc(), note="no matching PDF")
        print(f"{bar(i, len(MD_RAW))} {stem(md)} | no_pdf: copied unchanged"); continue
    print(f"{bar(i, len(MD_RAW))} {stem(md)} | {n_pages(pdf)} pages")
    for batch in pages(pdf, max_pages=10):       # read PDF pages as images; never load a whole long PDF at once
        raw = text in md for the same pages      # match by text on first and last page of batch; md may lack page markers
        append(out, optimise(raw, batch))        # see Markdown optimisation; append only, never overwrite earlier batches
        print(f"    pages {first}-{last} of {n_pages(pdf)} | tables rebuilt {n_tables}")
    append(out, "<!-- md_opt: model=...; date=YYYY-MM-DD; md_sha256=...; pdf_sha256=...; pdf_pages=N; fixes=...; unresolved=... -->")
    log_md(stem(md), "done", n_pages(pdf), n_tables, n_fixes, unresolved, started, now_utc(), note)   # 1 line per finished paper; quote cells with commas
    print(f"    done | fixes {n_fixes} | unresolved {n_unresolved}")
run(f"python {CHECK} --step0")                  # see Checks
print(f"Step 0 done | {n_done} optimised, {n_skipped} skipped")

# Step 1: extract. One session per agent; this session handles only its own slug. Agents work independently.
if any MD_RAW file has no finished MD_OPT file: stop; tell the user to run Step 0 first
print(f"Step 1: extract | agent {slug} | {len(PAPERS)} papers")
if not exists(RESULT):
    write(RESULT, [name for name, rule in COLUMNS])   # header only; do not copy example rows
    write(LOG, "paper,status,n_rows,started,finished,note," + TOKEN_COLS)
log("_run", "start", 0, now_utc(), "", f"model={AGENTS[slug]}; date=YYYY-MM-DD; git={git rev-parse HEAD}; claude_md_sha256=...; papers_sha256=...")   # 1 line per run
read(METADATA); read(TEMPLATE, rows=2..6 + first 3 rows with PJP mths filled)   # column rules + value format; TEMPLATE column order differs
for i, paper in enumerate(sorted(PAPERS), 1):
    if paper in LOG:                         # finished in an earlier run
        print(f"{bar(i, len(PAPERS))} {stem(paper)} | skipped: in LOG"); continue
    started = now_utc()
    remove rows of paper from RESULT         # leftovers from an interrupted run (match by File_name); state count in LOG note
    if broken(paper):                        # see Broken papers
        append(RESULT, na_row(paper, reason)); log(paper, "broken", 1, started, now_utc(), reason)
        print(f"{bar(i, len(PAPERS))} {stem(paper)} | broken: {reason}"); check_paper(paper); continue
    print(f"{bar(i, len(PAPERS))} {stem(paper)} | {n_pages(paper)} pages")
    for batch in pages(paper, max_pages=10): # never load a whole long paper at once
        append(RESULT, extract(batch))       # write after every batch
        print(f"    pages {first}-{last} of {n_pages(paper)} | rows {n_rows}")
    if n_rows == 0:                          # readable, but no relevant data
        append(RESULT, na_row(paper, reason)); log(paper, "no_data", 1, started, now_utc(), reason)
        print(f"    no_data: {reason}"); check_paper(paper); continue
    log(paper, "done", n_rows, started, now_utc(), problems)
    print(f"    done | rows {n_rows} | problems {len(problems)}")
    check_paper(paper)
print(f"Checks | agent {slug} | all papers")
run(f"python {CHECK} {slug}")                # see Checks
print(f"Step 1 done | agent {slug} | papers {n_done} done, {n_broken} broken, {n_no_data} no_data | rows {total_rows} | failed checks {n_failed}")
```

Hashes, run from the repo root, exactly: `papers_sha256` = `sha256sum data/papers_test/md_agents/*.md | LC_ALL=C sort | sha256sum`; `claude_md_sha256` = `sha256sum CLAUDE.md`. Record the first 64 characters of the output.

Token usage: do not estimate tokens. Every log line ends with 6 empty `TOKEN_COLS` cells. After the session, `USAGE` fills them per paper from the session transcript, using the `started` and `finished` times, so record both for every paper.

## Markdown optimisation

Compare each `MD_RAW` file with its PDF page by page. Fix the markdown so it matches the PDF.

- Tables: rebuild every table as a markdown pipe table, one species per row, values in the correct column. Fix rows split by wrapped species names, merged cells (`<br>` lists), and multi-line headers spread over several rows. Read tables from the PDF page, not from the broken markdown.
- Text: fix split ligatures (`fi re` -> `fire`, `fl ower` -> `flower`), OCR errors (`Brishane` -> `Brisbane`), joined words, and scrambled word order.
- Remove conversion junk: `<span id=...>` tags, stray OCR lines, and the `{N}` prefix before page markers.
- Put exactly one `<!-- PAGE BREAK -->` between PDF pages. Add markers where missing (OCR output has none).
- Keep all content, including title, authors, abstract, and references. Do not summarise, reorder sections, or add text that is not in the PDF.
- Value unreadable in the PDF: keep it as printed and list it under `unresolved` in the end comment. Table that cannot be rebuilt: list it as `unresolved=table N`.

## Extraction rules

- One row per species × study site × fire. Same species at two sites, or two fires at one site = two rows.
- Use only text in the paper. No background knowledge. No estimates.
- Value not stated in paper: leave cell empty.
- Species tables often span many pages. Read every page; extract every species row.
- Table continues into the next batch: reuse its column headers from the previous batch.
- Carry site and fire values (coordinates, location name, rainfall, fire season, severity, type) from the paper's methods onto every row of that paper. Several sites or fires: match each species row to its own site and fire.
- Several named sites share one set of coordinates: still 1 row per site; site name in `Location_name`, coordinates kept. Never merge sites into 1 row with per-site values in `Notes`.
- Site names: copy the name exactly as first printed in the paper's methods or study-site section. Do not add words (e.g. park or region name) and do not remove words. Map table codes (e.g. column `A`) to that name. Same site = same string on every row.
- A row needs at least 1 value in a fire response or time column. Values kept only in `Notes` (near-matches, unreliable or unitless values) never create a row on their own.
- Value given once for several sites (not split by site): the species recorded at 1 of those sites only -> value on that site's row. Recorded at 2 or more -> 1 extra row with `Location_name` = those site names joined by ` / `, coordinates empty; site-specific values stay on the site rows. Never put a shared value on one site's row when the species is recorded at several sites.
- Never merge rows. Same taxon printed as 2 or more separate entries (e.g. different references or variants): 1 row per entry; `Notes` of each starts with `separate entry in paper` and names what differs.
- Fill a column only when the paper's measure matches the column definition. Near-matches go in `Notes` only, with their definition (e.g. time to 80% of maximum flower production; expert or literature estimates).
- Measure defined as a percentage of a cohort or population flowering: 50% -> `Time to 50% flowering`, 80% -> `Time to 80% flowering`, whatever the paper calls it (e.g. maturity, primary juvenile period).
- `Time to 50% flowering_repr4` only for: maturation age measured as 50% of a cohort producing viable seed; or the primary-juvenile-period-in-months rule under Time columns.
- Not yet flowering at the last observation ("not flowering after 4 years"): `>N`, e.g. `>4`.
- Codes and units: use only definitions printed in the paper. Code not defined: copy it as printed (e.g. fire response `S`), never translate it. Unit not stated for a time value: leave the time columns empty; value and "unit not stated" in `Notes`.
- Tables may be parsed with one-off code. Then print 3 random parsed rows next to their source table lines and confirm they match before writing them.
- Ambiguous value: fill best reading, explain in `Notes`. Value printed with uncertainty marks (`c.`, `?`, `approx.`): fill the number without the marks; marks in `Notes`.
- Ambiguous column (paper does not say which measure a value is, e.g. not stated whether from seed or from resprouts): `Notes` only.
- Several estimates of one measure for the same species, site and fire (e.g. pooled model in a table and a single-site model in the text): fill the value from the paper's main results table; the others in `Notes`.

## Broken papers and papers without data

Every paper gets at least 1 row in `RESULT`. Write an NA row when:
- **broken**: file empty or under 1,000 bytes; no `<!-- md_opt:` end comment; end comment lists an `unresolved` table that holds species values; text garbled or unreadable; read error.
- **no_data**: paper readable, all pages read, no species-level juvenile period or fire response values found.

```python
na_row = {name: "NA" for name, rule in COLUMNS}  # exactly 1 NA row per paper
na_row["Notes"]  = reason                        # e.g. "empty markdown: PDF conversion failed"; "no data: review paper, no species values"
na_row["Source"] = citation if readable else stem(paper)
na_row["File_name"] = stem(paper)
```

Paper breaks partway: keep rows already extracted, add the 1 NA row, continue with next paper.

## Columns

Order in `RESULT`, grouped by similarity. Names match `TEMPLATE` exactly. Columns marked `new` are NA in `TEMPLATE` examples; fill them in `RESULT` when stated. Each column's definition, unit, allowed values and fill rule are in `METADATA` (same names, same order); follow them as part of these rules.

```python
COLUMNS = [
  # taxon
  ("Genus", ""),
  ("Species", ""),
  ("subsp", ""),
  ("scientific_name", ""),
  ("native_status", "new"),
  ("Family", ""),
  # fire response
  ("fire_response categorical_surv1", ""),
  ("resprouter_type", ""),
  # time after fire
  ("PJP mths", ""),
  ("primary_juvenile_period", ""),
  ("Age at first flower production from seed_repr3", ""),
  ("secondary_juvenile_period", ""),
  ("Time to first flower production resprout_repr3a", ""),
  ("Time to 50% flowering_repr4", ""),
  ("Time to 50% flowering", "new"),
  ("Time to 80% flowering", "new"),
  ("Recovery_time", "new"),
  ("Time_unit", "new"),
  # site
  ("Location_name", "new"),
  ("Latitude", ""),
  ("Longitude", ""),
  ("Rainfall_mm", ""),
  # fire
  ("Fire_type", "new"),
  ("Fire_season_categorical", ""),
  ("Fire_severity_categorical", ""),
  # record
  ("Notes", ""),
  ("Source", ""),
  ("File_name", "new"),
]
```

Time columns:
- Fixed units: `PJP mths` = months; `primary_juvenile_period`, `_repr3`, `_repr3a`, `_repr4` = years. All other time columns: paper's unit (days, weeks, months or years), recorded in `Time_unit`.
- Primary juvenile period in months: fill `PJP mths` (months) and `Time to 50% flowering_repr4` (years, no `Notes` entry). In years: fill `primary_juvenile_period` only.
- Fixed-unit column, value reported in another unit: convert to the column's unit (years = months / 12 = weeks / 52 = days / 365; months = weeks / 4.33 = days / 30.4); write `<column> converted from N <unit>` in `Notes`. No other conversion.
- Paper gives values under different terms (e.g. age at first flowering and primary juvenile period): each value in its own column. Apart from the months rule above, one value never fills 2 columns.
- Precision: copy values with exactly the decimals printed in the paper. Do not round or add trailing zeros (`3.0` stays `3.0`; `3` stays `3`). Converted value: paper or source states the value in the target unit -> copy it as printed. Otherwise round to 3 decimals, drop trailing zeros (26 months -> 2.167; 30 months -> 2.5; 48 months -> 4).
- Ranges: `min-max`, no spaces (`3.0 - 16.0` -> `3.0-16.0`). Open bounds as printed (`>23`, `<2`). Uncertain value: no `?` in the cell; explain in `Notes`.
- Variable-unit columns in one row use different units: `Time_unit` = unit of most values; list each exception in `Notes`, e.g. `Recovery_time in years`.
- Omit the 2 unnamed `TEMPLATE` columns (20 and 21). All 27 named `TEMPLATE` columns stay in `RESULT`, plus `native_status` (not in `TEMPLATE`): 28 columns.

CSV format: UTF-8, comma separator, LF line endings, decimal point `.`. Quote any cell containing a comma, quote, or newline; double inner quotes. Empty cell = no value; `NA` only in NA rows. Trim leading and trailing spaces in every cell (`TEMPLATE` has some; do not copy them). Dashes: ASCII hyphen `-` in every cell, including names, codes and `Source` (en dash `–` or em dash `—` -> `-`).

## Checks

`CHECK` tests every rule that needs no reading of the paper: header and column count, spaces, NA rows, `scientific_name`, coordinates, `Location_name`, time formats, decimals, `Time_unit`, `PJP mths` / 12 = repr4, fire season, rainfall, duplicates, `LOG` lines and row counts. It prints a summary, writes a report to `ROOT + "logs/"`, and exits 1 if any check fails.

```python
def check_paper(paper):                          # after every paper's LOG line, including broken and no_data; never skip
    for attempt in 1..3:
        if run(f"python {CHECK} {slug} --paper '{stem(paper)}'") == 0: return
        fix each failed row from the paper; fix LOG n_rows if rows changed
    log the remaining errors in the paper's LOG note
```

After all papers: run `CHECK` without `--paper`, fix errors the same way. After Step 0: run `CHECK --step0`, fix each failed `MD_OPT` file from its PDF. Warnings: look, fix if real. Never delete a row silently.

## Do not

- Read `data/reference/` or another agent's `RESULT` or `LOG`. They contain answers.
- Edit `TEMPLATE`, `METADATA`, `MD_RAW`, `PDF_DONE`, or anything in `data/papers_test/` outside `md_agents/`.
- Copy example rows from `TEMPLATE` into `RESULT`.
- Edit `CHECK`, or write any script file outside the session scratchpad.
- Create or write anything in `data/inference/`. Use `data/inference_test/` only.
