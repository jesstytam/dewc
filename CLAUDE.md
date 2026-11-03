# Data extraction pipeline

## Setup

```python
AGENTS   = {"opus-5-5": "claude-opus-5-5", "sonnet-5-5": "claude-sonnet-5-5"}   # slug: exact model ID; one session per agent
slug     = AGENTS key whose model ID is the model running this session   # not in AGENTS: stop and tell the user
MD_AGENT = "opus-5-5"                            # only this agent runs Step 0
RUN      = "test"                                # "test" = trial run; "full" = final run; keep "test" until the user says otherwise
ROOT     = {"test": "data/inference_test/", "full": "data/inference/"}[RUN]   # read references and write results only under ROOT
METADATA = ROOT + "references/metadata.csv"      # column dictionary: 1 row per RESULT column; type, unit, allowed values, trait code, definition, rule, example; ' | ' separates alternatives in allowed_values and example; the only format reference
VALUE_MAP = ROOT + "references/value_map.csv"   # paper terms and codes -> standard values for fire response, severity and resprouter type, with the notes entry to write
MD_RAW   = "data/papers_test/md_raw/*.md"        # 2_pdf2md.py output, every PDF; last line "<!-- pdf2md: scanned -->" or "<!-- pdf2md: text-layer -->"; Step 0 empties it
PDF_CLEAN = "data/papers_test/pdf_clean/{stem}.pdf"   # source PDF of each paper, renamed by 1_clean_pdf.py; same file stem as its markdown
MD_LLM   = "data/papers_test/md_llm/{stem}.md"   # Step 0 output; one file per paper: optimised (scanned) or moved unchanged (text-layer, end comment "md_opt: none")
PAPERS   = "data/papers_test/md_llm/*.md"        # extraction input; pages split by <!-- PAGE BREAK -->
RESULT   = ROOT + "results/{slug}_raw.csv"       # raw extraction, values as printed; header = COLUMNS names, in COLUMNS order (46 columns)
NORMALISE = "scripts/5_clean_results.py"  # RESULT -> final ROOT + "results/{slug}.csv" (units, case, dashes); run by the user after Step 1, never by agents
LOG      = ROOT + "logs/{slug}_log.csv"          # Step 1 log; header: paper,status,n_rows,started,finished,note + TOKEN_COLS
MD_LOG   = ROOT + "logs/md_opt_log.csv"          # Step 0 log; header: paper,status,pdf_pages,n_tables,n_fixes,unresolved,started,finished,note + TOKEN_COLS
TOKEN_COLS = "n_requests,input_tokens,cache_creation_input_tokens,cache_read_input_tokens,output_tokens,total_tokens"   # last 6 log columns; agents leave them empty, USAGE fills them
USAGE    = "scripts/4c_usage.py"          # token usage per paper; run by the user after each session, never by agents
CHECK    = "scripts/4a_check.py"          # fixed check script; run it, never edit it; writes reports to ROOT + "logs/"
```

## Read and write scope

| Step | Read | Write |
|---|---|---|
| 0 | `MD_RAW`, `PDF_CLEAN` | `.md` files in `data/papers_test/md_llm/`; move or remove `.md` files in `data/papers_test/md_raw/`; `MD_LOG`; `CHECK --step0` report |
| 1 | `METADATA`, `VALUE_MAP`, `PAPERS`, `RESULT`, `LOG` | `RESULT`, `LOG`; `CHECK` report |

Everything not listed for a step is off limits for that step. One-off shell or Python commands are allowed; a code file may be written only to the session scratchpad (never to the repo), so its full text stays in the session transcript.

## Steps

`print(...)` = write that status line to the chat as plain text, so the user can follow progress. `now_utc()` = output of `date -u +%FT%TZ`, e.g. `2026-10-02T08:04:26Z`. `bar(i, n)` = text progress bar, 20 characters wide: `[######--------------] 2/6 (33%)`.

```python
# Step 0: optimise markdown. Only in a session where slug == MD_AGENT; other sessions never run Step 0.
print(f"Step 0: optimise markdown | {len(MD_RAW)} papers")
if not exists(MD_LOG): write(MD_LOG, "paper,status,pdf_pages,n_tables,n_fixes,unresolved,started,finished,note," + TOKEN_COLS)
for i, md in enumerate(sorted(MD_RAW), 1):
    out = MD_LLM(stem(md))
    if exists(out) and out ends with "<!-- md_opt:":    # finished earlier, interrupted before md was removed
        remove(md); print(f"{bar(i, len(MD_RAW))} {stem(md)} | skipped: already done"); continue
    if exists(out): overwrite(out, "")           # unfinished file from an interrupted run: restart from page 1; status "restarted" in note
    started = now_utc()
    if md ends with "<!-- pdf2md: text-layer -->":   # text-layer PDF: no optimisation
        move(md, out); replace(out, last line, "<!-- md_opt: none; text-layer PDF, raw marker output, Step 0 skipped -->")
        log_md(stem(md), "text_layer", started=started, finished=now_utc())
        print(f"{bar(i, len(MD_RAW))} {stem(md)} | text_layer: moved unchanged"); continue
    pdf = PDF_CLEAN(stem(md))                    # md ends with "<!-- pdf2md: scanned -->"
    if not exists(pdf):                          # move md unchanged, add end comment with note
        move(md, out); replace(out, last line, "<!-- md_opt: ...; note=no matching PDF -->"); log_md(stem(md), "no_pdf", started=started, finished=now_utc(), note="no matching PDF")
        print(f"{bar(i, len(MD_RAW))} {stem(md)} | no_pdf: moved unchanged"); continue
    print(f"{bar(i, len(MD_RAW))} {stem(md)} | {n_pages(pdf)} pages")
    for batch in pages(pdf, max_pages=10):       # read PDF pages as images; never load a whole long PDF at once
        raw = text in md for the same pages      # match by text on first and last page of batch; md may lack page markers
        append(out, optimise(raw, batch))        # see Markdown optimisation; append only, never overwrite earlier batches
        print(f"    pages {first}-{last} of {n_pages(pdf)} | tables rebuilt {n_tables}")
    append(out, "<!-- md_opt: model=...; date=YYYY-MM-DD; md_sha256=...; pdf_sha256=...; pdf_pages=N; fixes=...; unresolved=... -->")
    log_md(stem(md), "done", n_pages(pdf), n_tables, n_fixes, unresolved, started, now_utc(), note)   # 1 line per finished paper; quote cells with commas
    remove(md)                                   # only after the end comment and MD_LOG line are written
    print(f"    done | fixes {n_fixes} | unresolved {n_unresolved}")
run(f"python {CHECK} --step0")                  # see Checks
print(f"Step 0 done | {n_done} optimised, {n_text_layer} text_layer, {n_skipped} skipped")

# Step 1: extract. One session per agent; this session handles only its own slug. Agents work independently.
if MD_RAW is not empty: stop; tell the user to run Step 0 first
print(f"Step 1: extract | agent {slug} | {len(PAPERS)} papers")
if not exists(RESULT):
    write(RESULT, [name for name, rule in COLUMNS])   # header only
    write(LOG, "paper,status,n_rows,started,finished,note," + TOKEN_COLS)
log("_run", "start", 0, now_utc(), "", f"model={AGENTS[slug]}; date=YYYY-MM-DD; git={git rev-parse HEAD}; claude_md_sha256=...; papers_sha256=...")   # 1 line per run
read(METADATA); read(VALUE_MAP)              # column rules, value formats, term map
for i, paper in enumerate(sorted(PAPERS), 1):  # LC_ALL=C order; one paper at a time: finish its LOG line before starting the next
    if paper in LOG:                         # finished in an earlier run
        print(f"{bar(i, len(PAPERS))} {stem(paper)} | skipped: in LOG"); continue
    started = now_utc()
    remove rows of paper from RESULT         # leftovers from an interrupted run (match by `file_name`); state count in LOG note
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
print(f"Step 1 done | agent {slug} | papers {n_done} done, {n_broken} broken, {n_no_data} no_data | rows {total_rows} | failed checks {n_failed} | next: user runs NORMALISE")
```

Hashes, run from the repo root, exactly: `papers_sha256` = `sha256sum data/papers_test/md_llm/*.md | LC_ALL=C sort | sha256sum`; `claude_md_sha256` = `sha256sum CLAUDE.md`. Record the first 64 characters of the output.

Tokens: never estimate. Leave the 6 `TOKEN_COLS` cells empty on every log line; record `started` and `finished` for every paper (`USAGE` uses them).

## Markdown optimisation

Compare each scanned paper's `MD_RAW` file with its PDF page by page. Fix the markdown so it matches the PDF. Raw text of a scanned PDF may be poor OCR or empty (no text layer): then build each page from the PDF page image. Do not copy the `<!-- pdf2md: ... -->` line into `MD_LLM`.

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
- Carry site and fire values (coordinates, location name, rainfall, fire season, severity, type) from the paper's methods onto every row of that paper. Several sites or fires: match each species row to its own site and fire. Value printed for the species itself (its table row or a sentence about it, e.g. 'low intensity' for one species): use it on that species' row instead of the paper-wide value; the paper-wide value in `notes`.
- Several named sites share one set of coordinates: still 1 row per site; site name in `location_name`, coordinates kept. Never merge sites into 1 row with per-site values in `notes`.
- A row needs at least 1 value in a fire response or time column. Values kept only in `notes` (near-matches, unreliable or unitless values) never create a row on their own. Exception: a fire response code left out of the cell by a `VALUE_MAP` rule (no clear class, conflicting codes) still creates a row.
- Value given once for several sites (not split by site): the species recorded at 1 of those sites only -> value on that site's row. Recorded at 2 or more -> 1 extra row with `location_name` = those site names joined by `; `, coordinates empty; site-specific values stay on the site rows. Never put a shared value on one site's row when the species is recorded at several sites.
- Never merge rows. Same taxon printed as 2 or more separate entries (e.g. different references or variants): 1 row per entry. Duplicate rows are fine; do not check or remove them.
- Fill a column only when the paper's measure matches the column definition. Near-matches go in `notes` only, with their definition (e.g. time to 80% of maximum flower production; expert or literature estimates).
- Choose the column by the paper's definition of the measure, not by its name. E.g. 'juvenile period' defined as the time for 50% of individuals to flower -> `time_to_50_percent_flowering`, not `primary_juvenile_period`; the paper's term and definition in `notes`. Columns with the same definition (`primary_juvenile_period` / `age_at_first_flower_production_from_seed_repr3`; `secondary_juvenile_period` / `time_to_first_flower_production_resprout_repr3a`): the paper's term decides, as in `METADATA`.
- Not yet flowering at the last observation ("not flowering after 4 years"): `>N` with its unit, e.g. `>4` + `years`.
- Codes and units: use only definitions printed in the paper. Code not defined: copy it as printed (e.g. fire response `S`), never translate it. Unit not stated for a time value: leave the time columns empty; value and "unit not stated" in `notes`.
- Tables may be parsed with one-off code. Then print 3 random parsed rows next to their source table lines and confirm they match before writing them.
- Ambiguous value: fill best reading, explain in `notes`. Value printed with uncertainty marks (`c.`, `?`, `approx.`): fill the number without the marks; marks in `notes`.
- Every place named in `data_location` gets its verbatim quote in `data_quote`: the sentence, the species' table row, or the figure label and title (see `METADATA`). Copy it from the paper's markdown, not from memory; `CHECK` searches the paper for it.
- Ambiguous column (paper does not say which measure a value is, e.g. not stated whether from seed or from resprouts): `notes` only.
- Several estimates of one measure for the same species, site and fire (e.g. pooled model in a table and a single-site model in the text): fill the value from the paper's main results table; the others in `notes`.

## Broken papers and papers without data

Every paper gets at least 1 row in `RESULT`. Write an NA row when:
- **broken**: file empty or under 1,000 bytes; no `<!-- md_opt:` end comment; end comment lists an `unresolved` table that holds species values; text garbled or unreadable; read error.
- Text-layer paper (end comment `md_opt: none`) broken because its text is garbled (e.g. wrong font encoding): LOG note starts with `needs Step 0:` and names the problem. The user then puts the paper back into `MD_RAW` marked `<!-- pdf2md: scanned -->` and runs Step 0 for it.
- **no_data**: paper readable, all pages read, no species-level juvenile period or fire response values found.

```python
na_row = {name: "NA" for name, rule in COLUMNS}  # exactly 1 NA row per paper
na_row["notes"]  = reason                        # e.g. "empty markdown: PDF conversion failed"; "no data: review paper, no species values"
na_row["source"] = citation if readable else stem(paper)
na_row["file_name"] = stem(paper)
na_row["supplementary_material"] = items if any else "NA"   # see Supplementary material
```

Paper breaks partway: keep rows already extracted, add the 1 NA row, continue with next paper.

Supplementary material (not in `PAPERS`): paper refers to supplementary or supporting material, or to items such as `Table S1`, `Appendix S2`, `Online Resource 1` -> fill `supplementary_material` on every row of that paper, NA row included (see `METADATA`). Extract what the main text gives; never guess the supplement's values.

## Columns

Order in `RESULT`, grouped by similarity. Names = the existing dataset's names after `janitor::clean_names()` (lower case, `_` for spaces, `%` -> `percent`); `new` = column not in it. Each column's definition, unit, allowed values, fill rule and example are in `METADATA` (same names, same order); follow them as part of these rules.

```python
COLUMNS = [
  # taxon
  ("genus", ""),
  ("species", ""),
  ("subsp", ""),
  ("scientific_name", ""),
  ("native_status", "new"),
  ("family", ""),
  # fire response
  ("fire_response_categorical_surv1", ""),
  ("fire_response_implied", "new"),
  ("resprouter_type", ""),
  # time after fire
  ("pjp_mths", ""),
  ("primary_juvenile_period", ""),
  ("primary_juvenile_period_unit", "new"),
  ("age_at_first_flower_production_from_seed_repr3", ""),
  ("age_at_first_flower_production_from_seed_repr3_unit", "new"),
  ("secondary_juvenile_period", ""),
  ("secondary_juvenile_period_unit", "new"),
  ("time_to_first_flower_production_resprout_repr3a", ""),
  ("time_to_first_flower_production_resprout_repr3a_unit", "new"),
  ("time_to_50_percent_flowering_repr4", ""),
  ("time_to_50_percent_flowering_repr4_unit", "new"),
  ("time_to_50_percent_flowering", "new"),
  ("time_to_50_percent_flowering_unit", "new"),
  ("time_to_80_percent_flowering", "new"),
  ("time_to_80_percent_flowering_unit", "new"),
  ("recovery_time", "new"),
  ("recovery_time_unit", "new"),
  # error of a time value
  ("error_column", "new"),
  ("error_type", "new"),
  ("error_value", "new"),
  ("sample_size", "new"),
  # site
  ("location_name", "new"),
  ("latitude", ""),
  ("longitude", ""),
  ("rainfall_mm", ""),
  ("rainfall_post_fire_mm", "new"),
  ("rainfall_post_fire_period", "new"),
  # fire
  ("fire_type", "new"),
  ("fire_season_categorical", ""),
  ("fire_severity_categorical", ""),
  # record
  ("data_location", "new"),
  ("data_quote", "new"),
  ("supplementary_material", "new"),
  ("notes", ""),
  ("source", ""),
  ("file_name", "new"),
  ("pdf_path", "new"),
]
```

Time columns (raw: as printed; `NORMALISE` converts):
- Each time column has a unit column after it (`<column>_unit`). Value cell: the value exactly as printed (number, `min-max` or `>`/`<` bound; same decimals, e.g. `3.0 - 16.0`, `>4`). Unit cell: `days`, `weeks`, `months` or `years` (the paper's unit, spelled out). E.g. `26` + `months`; `>4` + `years`. Never convert or round. Value filled = unit filled; no unit printed: both empty (see Extraction rules).
- Primary juvenile period in any unit: `primary_juvenile_period`. `NORMALISE` moves months to `pjp_mths`.
- Leave `pjp_mths`, `scientific_name` and `pdf_path` empty (NA row: `NA`); `NORMALISE` fills them.
- `error_value` in the unit of its time column as printed (that column's `_unit` cell); `NORMALISE` converts both.
- Paper prints one value in 2 units: write the one in the paper's main results; the other in `notes`.
- Paper gives values under different terms (e.g. age at first flowering and primary juvenile period): each value in its own column. One value never fills 2 columns.
- Uncertain value: no `?` in the cell; explain in `notes`.

CSV format: UTF-8, comma separator, LF line endings, decimal point `.`. Quote any cell containing a comma, quote, or newline; double inner quotes. Empty cell = no value; `NA` only in NA rows. Trim leading and trailing spaces in every cell. Case and dashes: copy as printed; `NORMALISE` sets them. Exception: `notes` in lower case, except codes (case can carry meaning, e.g. `R` vs `r`), genus names and quoted text. Several values in one cell: separate with `; ` (semicolon, space), e.g. `autumn; spring`; a `/` printed inside a single value (e.g. code `K/r`, a site name) stays as printed. Form not set by a rule: use the form of the `METADATA` example. Uncertain value: keep the format; explain in `notes`.

## Checks

`CHECK` tests the format rules that need no reading of the paper. It prints a summary, writes a report to `ROOT + "logs/"`, and exits 1 if any error is found.

```python
def check_paper(paper):                          # after every paper's LOG line, including broken and no_data; never skip
    for attempt in 1..3:
        if run(f"python {CHECK} {slug} --paper '{stem(paper)}'") == 0: return
        fix each failed row from the paper; fix LOG n_rows if rows changed
    log the remaining errors in the paper's LOG note
```

After all papers: run `CHECK` without `--paper`, fix errors the same way. After Step 0: run `CHECK --step0`, fix each failed `MD_LLM` file from its PDF. Warnings: look, fix if real. Never delete a row silently.

## Do not

- Read `data/reference/`, `data/papers_test/answers/`, `logs/benchmark*.csv`, or another agent's `RESULT` or `LOG`. They contain answers.
- Edit `METADATA`, `VALUE_MAP`, `PDF_CLEAN`, or anything in `data/papers_test/` outside `md_raw/` (Step 0 only: move or remove) and `md_llm/`.
- Edit `CHECK` or `NORMALISE`, run `NORMALISE`, or write the final `ROOT + "results/{slug}.csv"`.
- Write any script file outside the session scratchpad.
- Create or write anything in `data/inference/`. Use `data/inference_test/` only.
