# Data extraction pipeline

## Setup

```python
AGENTS   = {"opus-5-5": "claude-opus-5-5", "sonnet-5-5": "claude-sonnet-5-5"}   # slug: exact model ID
MD_AGENT = "opus-5-5"                            # only this agent runs Step 0
RUN      = "test"                                # "test" = trial run; "full" = final run
ROOT     = {"test": "data/inference_test/", "full": "data/inference/"}[RUN]   # read references and write results only under ROOT
TEMPLATE = ROOT + "references/template.csv"      # row 1 = header (28 columns); rows 2+ = worked examples; new columns = NA in examples
METADATA = ROOT + "references/metadata.csv"      # trait definitions
MD_RAW   = "data/papers_test/md/*.md"            # pdf2md.py output
PDF_DONE = "data/papers_test/pdf_done/*.pdf"     # source PDF for each MD_RAW file; same file stem
MD_OPT   = "data/papers_test/md_agents/{stem}.md" # Step 0 output; one file per paper
PAPERS   = "data/papers_test/md_agents/*.md"     # extraction input = MD_OPT; pages split by <!-- PAGE BREAK -->
RESULT   = ROOT + "results/{slug}.csv"           # header = COLUMNS names, in COLUMNS order (26 columns)
LOG      = ROOT + "results/{slug}_log.csv"       # header: paper,status,n_rows,note
SCRIPTS  = "scripts/pipeline/"                   # helper scripts for Step 1 only
```

## Read and write scope

| Step | Read | Write |
|---|---|---|
| 0 | `MD_RAW`, `PDF_DONE` | `.md` files in `data/papers_test/md_agents/` only |
| 1 | `METADATA`, `TEMPLATE`, `PAPERS` | `RESULT`, `LOG`, `SCRIPTS` |

Everything not listed for a step is off limits for that step.

## Steps

```python
# Step 0: optimise markdown. Run by MD_AGENT only, before Step 1.
for md in sorted(MD_RAW):
    out = MD_OPT(stem(md))
    if exists(out) and out ends with "<!-- md_opt:": continue   # finished earlier; resume safe
    if exists(out): overwrite(out, "")           # unfinished file from an interrupted run: restart from page 1
    pdf = PDF_DONE matching stem(md)             # no matching PDF: copy md unchanged, then add end comment with note
    for batch in pages(pdf, max_pages=10):       # read PDF pages as images; never load a whole long PDF at once
        raw = text in md for the same pages      # match by text on first and last page of batch; md may lack page markers
        append(out, optimise(raw, batch))        # see Markdown optimisation; append only, never overwrite earlier batches
    append(out, "<!-- md_opt: model=...; date=YYYY-MM-DD; md_sha256=...; pdf_sha256=...; pdf_pages=N; fixes=...; unresolved=... -->")

# Step 1: extract. Each agent works independently.
for slug, model in AGENTS.items():
    if not exists(RESULT):
        write(RESULT, [name for name, rule in COLUMNS])   # header only; do not copy example rows
        write(LOG, "paper,status,n_rows,note")
    log("_run", "start", 0, f"model={model}; date=YYYY-MM-DD; git={git rev-parse HEAD}; papers_sha256=...")   # 1 line per run
    read(METADATA); read(TEMPLATE, rows=2..6 + first 3 rows with PJP mths filled)   # definitions + value format; TEMPLATE column order differs
    for paper in sorted(PAPERS):
        if paper in LOG: continue                # finished in an earlier run
        remove rows of paper from RESULT         # leftovers from an interrupted run; state count in LOG note
        if broken(paper):                        # see Broken papers
            append(RESULT, na_row(paper, reason)); log(paper, "broken", 1, reason); continue
        for batch in pages(paper, max_pages=10): # never load a whole long paper at once
            append(RESULT, extract(batch))       # write after every batch
        if n_rows == 0:                          # readable, but no relevant data
            append(RESULT, na_row(paper, reason)); log(paper, "no_data", 1, reason); continue
        log(paper, "done", n_rows, problems)
    check(RESULT)                                # see Checks
```

`papers_sha256` = sha256 of the sorted `sha256sum` output of all `PAPERS` files.

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
- Ambiguous value: fill best reading, explain in `Notes`.

## Broken papers and papers without data

Every paper gets at least 1 row in `RESULT`. Write an NA row when:
- **broken**: file empty or under 1,000 bytes; no `<!-- md_opt:` end comment; end comment lists an `unresolved` table that holds species values; text garbled or unreadable; read error.
- **no_data**: paper readable, all pages read, no species-level juvenile period or fire response values found.

```python
na_row = {name: "NA" for name, rule in COLUMNS}  # exactly 1 NA row per paper
na_row["Notes"]  = reason                        # e.g. "empty markdown: PDF conversion failed"; "no data: review paper, no species values"
na_row["Source"] = citation if readable else stem(paper)
```

Paper breaks partway: keep rows already extracted, add the 1 NA row, continue with next paper.

## Columns

Order in `RESULT`, grouped by similarity. Names match `TEMPLATE` exactly. Columns marked `new` are NA in `TEMPLATE` examples; fill them in `RESULT` when stated.

```python
COLUMNS = [
  # taxon
  ("Genus", "as printed in paper"),
  ("Species", "as printed in paper"),
  ("subsp", "subspecies or variety name; '*' if species introduced / exotic / weed"),
  ("scientific_name", "Genus + ' ' + Species (+ ' *' if introduced)"),
  ("Family", "as printed; empty if not stated"),
  # fire response
  ("fire_response categorical_surv1", "obligate | resprouter; paper gives both for one species -> paper's code as printed, e.g. 'R / k'"),
  ("resprouter_type", "e.g. basal, epicormic, lignotuber; as printed"),
  # time after fire: value as printed; range as 'min-max', e.g. 3.0-4.0; see Time columns
  ("PJP mths", "primary juvenile period, paper reports it in months"),
  ("primary_juvenile_period", "primary juvenile period, paper reports it in years"),
  ("Age at first flower production from seed_repr3", "years; time or age to first flowering from seed, other wording"),
  ("secondary_juvenile_period", "paper's term is 'secondary juvenile period'"),
  ("Time to first flower production resprout_repr3a", "years; time to first flowering or reproduction of resprouts, other wording"),
  ("Time to 50% flowering_repr4", "years; maturation age: time for 50% of an even-aged cohort to produce first viable seed; flowering-based estimates accepted, method in Notes"),
  ("Time to 50% flowering", "new; time until 50% of individuals flower, as stated in paper; not maturation age"),
  ("Time to 80% flowering", "new; time until 80% of individuals flower"),
  ("Recovery_time", "new; time from fire until recovery as defined in paper; recovery measure in Notes, e.g. 'pre-fire cover'"),
  ("Time_unit", "new; months | years; unit of secondary_juvenile_period, Time to 50% flowering, Time to 80% flowering, Recovery_time; empty if none filled"),
  # site
  ("Location_name", "new; study site name as printed; fill only if Latitude and Longitude both empty"),
  ("Latitude", "decimal degrees, WGS84; south negative; 33° 45' S -> -33.75"),
  ("Longitude", "decimal degrees, WGS84; east positive"),
  ("Rainfall_mm", "rainfall of location, mm; mean annual if stated; other period (e.g. post-fire year) -> period in Notes"),
  # fire
  ("Fire_type", "new; wildfire | prescribed burn | experimental burn | as printed"),
  ("Fire_season_categorical", "Summer | Autumn | Winter | Spring; several seasons joined by '/', e.g. Autumn/Spring; derive from fire date if only date given, note in Notes"),
  ("Fire_severity_categorical", "Low | Moderate | Moderate-High | High; other scale -> as printed"),
  # record
  ("Notes", "assumptions, ambiguities, page number of source table"),
  ("Source", "full citation of the paper, same string on every row of that paper"),
]
```

Time columns:
- Fixed units: `PJP mths` = months; `primary_juvenile_period`, `_repr3`, `_repr3a`, `_repr4` = years. All other time columns: paper's unit, recorded in `Time_unit`.
- Primary juvenile period in months: fill `PJP mths` (months) and `Time to 50% flowering_repr4` (years, no `Notes` entry). In years: fill `primary_juvenile_period` only.
- `_repr3`, `_repr3a`, `_repr4` value reported in months: divide by 12; write `<column> converted from N months` in `Notes`. No other conversion.
- Paper gives values under different terms (e.g. age at first flowering and primary juvenile period): each value in its own column. Apart from the months rule above, one value never fills 2 columns.
- Precision: copy values with exactly the decimals printed in the paper. Do not round or add trailing zeros (`3.0` stays `3.0`; `3` stays `3`). Converted value: paper or source states the value in the target unit -> copy it as printed. Otherwise round to 3 decimals, drop trailing zeros (26 months -> 2.167; 30 months -> 2.5; 48 months -> 4).
- Ranges: `min-max`, no spaces (`3.0 - 16.0` -> `3.0-16.0`). Open bounds as printed (`>23`, `<2`). Uncertain value: no `?` in the cell; explain in `Notes`.
- Variable-unit columns in one row use different units: `Time_unit` = unit of most values; list each exception in `Notes`, e.g. `Recovery_time in years`.
- Omit the 2 unnamed `TEMPLATE` columns (20 and 21). All 26 named columns stay in `RESULT`.

CSV format: UTF-8, comma separator, LF line endings, decimal point `.`. Quote any cell containing a comma, quote, or newline; double inner quotes. Empty cell = no value; `NA` only in NA rows. Trim leading and trailing spaces in every cell (`TEMPLATE` has some; do not copy them).

## Checks

```python
for row in RESULT:
    assert n_columns(row) == 26
    assert row["Source"]
    if row["Genus"] == "NA": assert row["Notes"]; continue    # NA row: broken or no_data paper
    assert row["Genus"] and row["Species"]
    assert -44 <= row["Latitude"] <= -10 and 112 <= row["Longitude"] <= 154    # if filled
    assert row["Location_name"] == "" or (row["Latitude"] == "" and row["Longitude"] == "")
    assert row["Time_unit"] in {"months", "years"} if any variable-unit time column filled
    assert every time value matches r"[<>]?\d+(\.\d+)?(-\d+(\.\d+)?)?"    # if filled
assert no duplicate (scientific_name, Latitude, Longitude, Location_name, Fire_type, Fire_season_categorical, Source)
assert every paper in PAPERS has >= 1 row in RESULT and 1 line in LOG
```

Failed check: fix row from the paper, or log the problem. Never delete a row silently.

## Do not

- Read `data/reference/` or another agent's `RESULT` or `LOG`. They contain answers.
- Edit `TEMPLATE`, `METADATA`, `MD_RAW`, `PDF_DONE`, or anything in `data/papers_test/` outside `md_agents/`.
- Copy example rows from `TEMPLATE` into `RESULT`.
