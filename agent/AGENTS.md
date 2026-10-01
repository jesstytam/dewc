# Data extraction pipeline

## Setup

```python
AGENTS   = {1: "Opus 5.5", 2: "Sonnet 5.5"}      # slug: "opus-5-5", "sonnet-5-5"
RUN      = "test"                                # "test" = trial run; "full" = final run
ROOT     = {"test": "data/inference_test/", "full": "data/inference/"}[RUN]   # read references and write results only under ROOT
TEMPLATE = ROOT + "references/template.csv"      # row 1 = header (27 columns); rows 2+ = worked examples from paper(s) in PAPERS; new columns = NA in examples
METADATA = ROOT + "references/metadata.csv"      # trait definitions
PAPERS   = "data/papers/md/*/*.md"               # one folder per paper; pages split by <!-- PAGE BREAK -->
RESULT   = ROOT + "results/{slug}.csv"            # header = COLUMNS names, in COLUMNS order (25 columns)
LOG      = ROOT + "results/{slug}_log.csv"       # paper, status, n_rows, note
SCRIPTS  = "scripts/pipeline/"                   # save helper scripts here
```

## Steps

```python
for agent in AGENTS:                              # agents work independently
    write(RESULT, [name for name, rule in COLUMNS])   # header only; do not copy example rows
    read(METADATA); read(TEMPLATE, rows=2..6)     # learn definitions + value format; TEMPLATE column order differs
    for paper in sorted(PAPERS):
        if broken(paper):                         # see Broken papers
            append(RESULT, na_row(paper, reason)); log(paper, "broken", 1, reason); continue
        for batch in pages(paper, max_pages=10):  # never load a whole long paper at once
            append(RESULT, extract(batch))        # write after every batch
        if n_rows == 0:                           # readable, but no relevant data
            append(RESULT, na_row(paper, reason)); log(paper, "no_data", 1, reason); continue
        log(paper, "done", n_rows, problems)
    check(RESULT)                                 # see Checks
```

## Extraction rules

- One row per species × study site. Same species at two sites = two rows.
- Use only text in the paper. No background knowledge. No estimates.
- Value not stated in paper: leave cell empty.
- Species tables often span many pages. Read every page; extract every species row.
- Carry site and fire values (coordinates, location name, rainfall, fire season, severity, type) from the paper's methods onto every row of that paper. Several sites or fires: match each species row to its own site and fire.
- Ambiguous value: fill best reading, explain in `Notes`.

## Broken papers and papers without data

Every paper gets at least 1 row in `RESULT`. Write an NA row when:
- **broken**: markdown empty or under 1,000 bytes; text garbled or unreadable; tables lost in conversion; read error.
- **no_data**: paper readable, all pages read, no species-level juvenile period or fire response values found.

```python
na_row = {name: "NA" for name, rule in COLUMNS}            # exactly 1 NA row per paper
na_row["Notes"]  = reason                         # e.g. "empty markdown: PDF conversion failed"; "no data: review paper, no species values"
na_row["Source"] = paper_folder_name
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
  ("fire_response categorical_surv1", "obligate | resprouter | paper's own code if mixed"),
  ("resprouter_type", "e.g. basal, epicormic, lignotuber; as printed"),
  # time after fire: value as printed; range as 'min-max', e.g. 3.0-4.0
  ("PJP mths", "primary juvenile period"),
  ("primary_juvenile_period", "time for plants from seed to flower after fire"),
  ("Age at first flower production from seed_repr3", "age at first flowering from seed"),
  ("secondary_juvenile_period", "time for resprouting plants to flower after fire"),
  ("Time to first flower production resprout_repr3a", "time to first reproduction after fire, resprouting taxa"),
  ("Time to 50% flowering_repr4", "time until 50% of individuals flower"),
  ("Time to 80% flowering", "new; time until 80% of individuals flower"),
  ("Recovery_time", "new; time from fire until recovery as defined in paper; recovery measure in Notes, e.g. 'pre-fire cover'"),
  ("Time_unit", "new; months | years; unit used by the paper for the time values in this row"),
  # site
  ("Location_name", "new; study site name as printed; fill only if Latitude and Longitude both empty"),
  ("Latitude", "decimal degrees, WGS84; south negative; 33° 45' S -> -33.75"),
  ("Longitude", "decimal degrees, WGS84; east positive"),
  ("Rainfall_mm", "rainfall of location, mm; mean annual if stated; other period (e.g. post-fire year) -> period in Notes"),
  # fire
  ("Fire_type", "new; wildfire | prescribed burn | experimental burn | as printed"),
  ("Fire_season_categorical", "Summer | Autumn | Winter | Spring; derive from fire date if only date given, note in Notes"),
  ("Fire_severity_categorical", "Low | Moderate | Moderate-High | High; other scale -> as printed"),
  # record
  ("Notes", "assumptions, ambiguities, page number of source table"),
  ("Source", "full citation of the paper, same string on every row of that paper"),
]
```

Time units:
- Keep time values in the unit the paper uses. Do not convert.
- Record that unit in `Time_unit`. Unit in a column name (e.g. "PJP mths") does not apply.
- Paper uses different units for different values in one row: `Time_unit` = unit of most values; list each exception in `Notes`, e.g. `Recovery_time in years`.
- Omit the 3 unnamed `TEMPLATE` columns.

## Checks

```python
for row in RESULT:
    assert n_columns(row) == 25                   # quote any cell containing a comma
    if row["Genus"] == "NA": assert row["Notes"]; continue    # NA row: broken or no_data paper
    assert row["Genus"] and row["Species"] and row["Source"]
    assert -44 <= row["Latitude"] <= -10 and 112 <= row["Longitude"] <= 154    # if filled
    assert row["Location_name"] == "" or (row["Latitude"] == "" and row["Longitude"] == "")
    assert row["Time_unit"] in {"months", "years"} if any time value filled
assert no duplicate (scientific_name, Latitude, Longitude, Source)
assert every paper in PAPERS has >= 1 row in RESULT and 1 line in LOG
```

Failed check: fix row from the paper, or log the problem. Never delete a row silently.

## Do not

- Read `data/reference/` or another agent's `RESULT`. They contain answers.
- Edit `TEMPLATE`, `METADATA`, or files under `data/papers/`.
- Copy example rows from `TEMPLATE` into `RESULT`.
