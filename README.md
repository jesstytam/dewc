# **D**ata **e**xtraction **w**ith **C**laude

## Installation

Clone this repo to have all scripts and files locally on your machine:
```
git clone git@github.com:jesstytam/primary_juvenile_meta-analysis.git
cd primary_juvenile_meta-analysis
```
Create an environment if you haven't got one already, e.g. using Anaconda or Miniconda:
```
conda create -n myenv python=3.12
conda activate myenv
```
And then install the dependencies:
```
pip install -r requirements.txt
```

## My system's setup

- System: Ubuntu 26.04.1 LTS
- LLM: Claude Code via the terminal
- Languages: Python, shell/bash script, R, natural language

## Data extraction with LLM

### Converting PDF to Markdown

Markdown is currently one of the better formats for LLMs to analyse, we first convert the PDFs to Markdown files. Here, I used the Python module [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) for conversion, which showed success for both text-based and image-based (scanned) PDFs.

### Important considerations

Since Claude / LLM is responsible for data extraction, the pipeline instructions were create through a back-and-fourth conversation with the chatbot. This was done by first having a simple outline of the requirements, including the following:

- input and output formats
- log files, what to log, e.g. token usage and terminal outputs
- reference materials, e.g. metadata
- language requirements, i.e. use of code and pseudo-code for deterministic outputs
- read and write permissions for which files and folders

### Writing CLAUDE.md

Claude reads instructions from the `CLAUDE.md` file, which was updated iteratively by parsing prompts to the LLM and manually checking the outputs after each inference test. 

To update the file, a CSV file containing the extraction results of 1 paper, as well as the associated metadata CSV file - both created by human, were provided to Claude for understanding the aims and requirements of the data extraction pipeline.

Requirements included some of the following:

- updating the variables and corresponding metadata required in this study from [Austraits](https://austraits.org/) and [Fire Ecology Database](http://fireecologyplants.net/).
- optimising the markdown output after converting PDFs to MDs with `1_pdf2md.py`
- data type inconsistencies, e.g. decimal places, to include "subsp." in subspecies column or not, etc.

Additional Python scripts created by Claude as per my instructions include the following:

- `4a_check.py` to identify conflicting results between inference outputs and guidelines
- `4b_log_session.py` to log each inference session's outputs
- `4c_usage.py` to record LLM token usage.
- `6_benchmark.py` to compare the results between the ground truth and results produced by the LLMs
- `6a_taxon_map.R` to align taxon names in the ground truth and the LLM results with the Australian Plant Census (APCalign), so synonyms match in `6_benchmark.py` (run `6_benchmark.py --taxa` first, then `--rescore`)

### Initial testing

The intial testing stage aimed to confirm and test that the outputs of the LLMs are consistent and follow the provided guidelines in `CLAUDE.md` while showing 0 errors when running `4a_check.py`. 

I first provided 1 paper that has been extracted already as an example. I then provided 6 papers that required extraction to update `CLAUDE.md` and test the pipeline. After a few trials, I added another 14 papers for further testing.

<image src="assets/pipeline_flowchart.drawio.png"/>

### Logging each session

Every pipeline session is logged automatically. A `SessionEnd` hook in `.claude/settings.json` runs `scripts/claude/4b_log_session.py` when a session ends. It acts only on sessions whose prompt starts with `Run Step 0` or `Run Step 1`; other sessions are ignored. For each pipeline session it:

1. copies the session transcript (which records the model of every response) and a snapshot of the step's outputs to `data/inference_test/logs/runs/<step>_<slug>_<session id>/`: `md_opt_log.csv` and `md_opt_check.csv` for Step 0; `<slug>_raw.csv`, `<slug>_log.csv` and `<slug>_check.csv` for Step 1;
2. adds one line to `data/inference_test/logs/sessions.csv`: date, step (`step0`, `step1-trial` or `step1`), agent, the model IDs that actually answered, Claude Code version, session ID;
3. fills the token breakdown (`n_requests`, `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`, `total_tokens`): per paper in that paper's line of the step's log, and per step as whole-session totals in `sessions.csv`. The session total minus the papers is setup, checks and wrap-up. Each request is assigned to a paper by the `started` and `finished` times the agent writes in its log. Cache-read tokens make up most of the total because every request re-reads the conversation so far; compare papers mainly on `output_tokens` and `n_requests`.

`models` in `sessions.csv` must show only the expected model ID (e.g. `claude-opus-5-5`). Any other model means the session did not run on the intended model, so its results are not valid for that agent. The agents also record the model themselves: Step 0 in the end comment of each optimised `md_llm/` file, Step 1 in the `_run` line of `<slug>_log.csv`.

Optional: before ending a session, type `/export data/inference_test/logs/runs/<step>_<slug>_<YYYYMMDD-HHMM>.txt` to also keep the conversation as readable text.

If the hook did not run (e.g. the terminal was killed), log the session by hand; running it twice is safe:

```bash
python scripts/claude/4b_log_session.py --session <session id>
```

**Before rerunning a step**, move that agent's live files out of the way, because papers already in the log are skipped. Their snapshot is already in `logs/runs/`. For Step 1: `data/inference_test/results/<slug>_raw.csv` (and the normalised `<slug>.csv`), `data/inference_test/logs/<slug>_log.csv` and `data/inference_test/logs/<slug>_check.csv`.

### Running

#### Preparation



#### Extraction

Use 1 model per Claude instance to prevent results leakage across models during inference times. Start a fresh instance for every step below. The pipeline rules are in `CLAUDE.md`, which Claude Code loads automatically; each session works out its agent from the model it runs on.

Step 1 reads the optimised papers in `data/papers_test/md_llm/`; `data/papers_test/md_raw/` must be empty.

1a. **Data extraction (Opus).** New session. Papers already in the log are skipped.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions.
   ```

1b. **Data extraction (Sonnet).** New session, same prompt.

   ```
   claude --model claude-sonnet-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions.
   ```

2. **Normalise.** Converts the raw results (values as printed) into the final results: time values (value + `<column>_unit` cells) to each column's unit, `pjp_mths`, case, dashes, `scientific_name` and `pdf_path`. Writes `data/inference_test/results/<slug>.csv`; the raw file is not changed. Rerun it after any change to the script; no re-extraction needed.

   ```
   python scripts/pipeline/5_normalise.py opus-5-5 sonnet-5-5
   ```

3. **Final check.** Each check exits 1 if any check fails; the reports are in `data/inference_test/logs/` (`<slug>_check.csv` for raw, `<slug>_check_final.csv` for final).

   ```
   python scripts/claude/4a_check.py opus-5-5
   python scripts/claude/4a_check.py sonnet-5-5
   python scripts/claude/4a_check.py opus-5-5 --final
   python scripts/claude/4a_check.py sonnet-5-5 --final
   ```

If a session stops early (usage limit, context full), start a new session with the same prompt. Finished papers are skipped and unfinished ones are redone.

All output stays in `data/inference_test/`. Nothing is written to `data/inference/` until the test run is complete.

### Benchmarking

I spent a good few weeks thinking about how to benchmark the extraction results against the ground truth, using methods such as F1 and Levenshtein distance. However, after more thinking, I realised that since 100% accuracy is only a theoretical number, as even a human produces around 4-5% error rates, there is no need to optimise the model(s) any further (currently at ~80% accurate). The biggest time lag in this pipeline can be cut even shorter if I can somehow reduce the time taken for a human to review the extraction results.

Nevertheless, it is always important to check that results produced by LLMs are of high quality. 

#### Ground truth

The ground truth is the human-extracted dataset in `data/papers_test/answers/juvenile_period_data_part*.ods`, which I checked against the papers. The rules are:

- Answer rows are matched to papers by the `Path` column, whose file stem equals `file_name` in the results.
- An empty cell means the paper does not state that value, so a model value in that cell counts as an error.
- Papers without answer rows are not scored. That leaves 19 of the 22 test papers (`Enright_et_al_1998`, `NSWNPWS_2004` and `Ooi_2019` are not scored).
- Remaining human errors in the ground truth were left in. The benchmark only needs to compare runs and models, as a human reviews every output anyway.
- `CLAUDE.md` forbids agents from reading the ground truth or the benchmark files during extraction.

#### Methods

`scripts/claude/6_benchmark.py` scores each Step 1 snapshot in `data/inference_test/logs/runs/` at 2 levels:

- **Taxa:** the set of taxa (genus + species + subspecies) of each paper. A true positive (TP) is a taxon on both sides, a false positive (FP) is a taxon only in the model's results, and a false negative (FN) is a taxon only in the ground truth.
- **Values:** for each taxon on both sides, the values of a column are pooled over the taxon's rows into a set on each side. A TP is a value on both sides, a FP is a model value not in the ground truth, and a FN is a ground truth value the model lacks.

Precision is TP / (TP + FP) and recall is TP / (TP + FN). The headline score is F0.5, which weights precision twice as much as recall, because a wrong value in a meta-analysis is worse than a missing value that a human reviewer can add. `precision_filled` is precision over cells that both sides filled, which separates wrong values from values the ground truth leaves empty.

Only papers extracted in the run itself are scored, so papers carried over from an earlier run are not counted twice. Because values are pooled per taxon, the value scores do not test whether a value sits on the correct site or fire row.

14 columns are scored at the value level, plus an `introduced` flag. The other result columns are not in the ground truth, so they are not scored. Two values are equal under these rules:

| Column | Rule |
|---|---|
| Taxon | Lower case, marks removed, compared on APC accepted names from `6a_taxon_map.R`; otherwise edit distance of at most 2 within the genus |
| Time columns, `rainfall_mm` | Uncertainty marks (`c.`, `~`, `?`) removed; same bound and range form; equal within half a unit of the coarser printed precision, at most 0.05 |
| `secondary_juvenile_period`, `time_to_50_percent_flowering` | As above, after conversion to years |
| `latitude`, `longitude` | Decimal degrees, equal within 0.01 |
| `fire_response_categorical_surv1` | Same class (obligate, O/R or resprouter) in `references/fire_response_pct.csv`; the paper's own code definition goes first; codes without a class must match exactly |
| `resprouter_type`, `fire_severity_categorical` | Each term compared in lower case; exact (singular for `resprouter_type`) |
| `fire_season_categorical` | All seasons of the cell, sorted; exact |
| `introduced` | Flag from `native_status` or a `*` in the name |

To reproduce the scores, run these commands from the repository root:

```
python scripts/claude/6_benchmark.py --taxa      # list taxon names
Rscript scripts/claude/6a_taxon_map.R            # map them to APC accepted names
python scripts/claude/6_benchmark.py --rescore   # score all runs
python scripts/claude/6_benchmark.py --report    # per-paper and per-column scores
```

The outputs are in `data/inference_test/logs/`: `benchmark.csv` (scores per run, paper and column), `benchmark_papers.csv` (latest run of each paper) and `benchmark_details.csv` (every taxon or value found on only one side).

#### Results

These are the latest runs of 2026-10-30 (git `f88b67e`), opus-5-5 run `54dd58ca` and sonnet-5-5 run `98e0ff1b`. Opus was scored on 18 papers, as `Ashton_et_al_1989` was started before its `_run` log line and so was left out. That paper adds only 1 missed taxon to the Sonnet totals and no values.

| Level | Agent | TP | FP | FN | Precision | Recall | F0.5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Taxa | Opus | 1027 | 79 | 83 | 0.93 | 0.93 | 0.93 |
| Taxa | Sonnet | 1027 | 68 | 84 | 0.94 | 0.92 | 0.94 |
| Values | Opus | 5646 | 423 | 1204 | 0.93 | 0.82 | 0.91 |
| Values | Sonnet | 5881 | 364 | 969 | 0.94 | 0.86 | 0.92 |

`Kubiak_2009` holds about 71% of the ground truth values, so it dominates these totals:

| Papers | Agent | Precision | Recall | F0.5 |
|---|---|---:|---:|---:|
| `Kubiak_2009` only | Opus | 0.99 | 0.92 | 0.98 |
| `Kubiak_2009` only | Sonnet | 0.99 | 0.97 | 0.99 |
| All others | Opus | 0.75 | 0.59 | 0.71 |
| All others | Sonnet | 0.78 | 0.59 | 0.73 |

Values by column:

| Column | Opus precision | Opus recall | Sonnet precision | Sonnet recall |
|---|---:|---:|---:|---:|
| `fire_response_categorical_surv1` | 0.99 | 0.96 | 0.99 | 0.96 |
| `primary_juvenile_period` | 0.95 | 0.96 | 0.96 | 0.96 |
| `secondary_juvenile_period` | 0.96 | 0.96 | 0.98 | 0.98 |
| `age_at_first_flower_production_from_seed_repr3` | 0.92 | 0.86 | 0.92 | 0.86 |
| `time_to_first_flower_production_resprout_repr3a` | 0.98 | 0.84 | 0.99 | 0.84 |
| `resprouter_type` | 0.81 | 0.56 | 0.93 | 0.56 |
| `latitude` | 0.97 | 0.65 | 0.99 | 0.76 |
| `longitude` | 0.98 | 0.65 | 0.99 | 0.76 |
| `rainfall_mm` | 0.36 | 0.85 | 0.36 | 0.85 |
| `fire_season_categorical` | 0.98 | 0.98 | 0.98 | 0.98 |
| `fire_severity_categorical` | 1.00 | 0.95 | 1.00 | 0.95 |
| `introduced` | 0.92 | 0.99 | 0.92 | 0.99 |
| `pjp_mths` | - | 0.00 | - | 0.00 |
| `time_to_50_percent_flowering_repr4` | - | 0.00 | - | 0.00 |
| `time_to_50_percent_flowering` | 0.00 | - | 0.00 | - |

Most of the low scores come from a few differences in convention, not from misread values:

- **Flowering columns:** both models put 50% flowering values in `time_to_50_percent_flowering` (70 FP), but the ground truth has them in `time_to_50_percent_flowering_repr4` (63 FN) and, for `Burrows_et_al_2008`, also in `pjp_mths` (53 FN). `Burrows_et_al_2008` is the largest source, followed by `Benson_1985` and `Miller_et_al_2025`. This explains the 3 columns with a score of 0.
- **`Wark_1997` rainfall:** both models give 657 mm on every row (about 160 FP), which the ground truth leaves empty. This explains the low `rainfall_mm` precision.
- **`Wark_1997` coordinates:** the ground truth holds coordinates estimated from a map, which the models do not extract (about 160 FN each for latitude and longitude).
- **`Kubiak_2009` coordinates:** Opus left 136 rows empty and Sonnet left 22. This explains most of the gap between the 2 models.

Sonnet scored slightly higher than Opus on these runs, mainly because of the Kubiak coordinates. The difference is small, and both models need the human review step below.

### Token usage

**I believe that it is more important to calculate AI usage based on the number of tokens (an environment-centric approach), rather than cost (a capatalistic approach)**. This makes it easier to convert tokens to CO_2 / Wh / Litres of water, which puts things into perspective on the trade-offs of AI usage. 

Optimising Markdown files of scanned PDFs: 0.5-15M tokens per paper
Data extraction: ~ slightly more than 1M tokens for both models

See the AI disclosure section for a full breakdown of the token usage of this project. 

## Human-in-the-loop GUI

See [ryer](https://github.com/jesstytam/ryer) for a PyQt-based GUI to speed up the checking your extracted results.

## Adapting Claude for your meta-analysis

Different research projects have different data extraction needs. Given that LLMs are not deterministic, obviously, adapting the methods here will not yield identical performances. Nonetheless, I have asked Claude to write up some instructions below in this section to help best reproduce this repo, especially CLAUDE.md for other data extraction tasks.

### What Claude reckons

[ADAPTING_CLAUDE_MD.md](ADAPTING_CLAUDE_MD.md) builds this kind of pipeline for another meta-analysis. It is self-contained, so it does not need this repository. It needs 1 paper that has already been extracted by hand:

- `example.csv`: all rows of that paper, with the columns the new study needs
- `example.pdf`: the paper itself

Copy those files into an empty folder and start Claude Code there:

```bash
mkdir new_study && cd new_study
cp /path/to/ADAPTING_CLAUDE_MD.md /path/to/example.csv /path/to/example.pdf .
claude "Follow ADAPTING_CLAUDE_MD.md. Example extraction: example.csv. Example paper: example.pdf."
```

Claude reads the example, works out the row unit, columns and value formats, and asks about anything the example cannot show. You approve `metadata.csv`. Claude then writes `CLAUDE.md` and the scripts, and tests them against the example.

After that, you run the pilot extractions it describes, one fresh session per model. Most of the rules in this repository's `CLAUDE.md` came from pilot disagreements rather than upfront design, so expect several rounds.

## AI disclosure

Needless to say, this project was made *heavily* with the assistance of Anthropic's Claude.

Claude estimates that this project has used about 1.0 billion tokens as of 2026-11-03, summed from the local Claude Code session transcripts (52 sessions, about 4,000 API requests; about 2,760 by Claude Opus 5.5 and 1,220 by Claude Sonnet 5.5):

| Token type | Tokens |
|---|---|
| Input | 7,959 |
| Cache creation | 21.3M |
| Cache read | 977.4M |
| Output | 4.3M |
| **Total** | **~1.003B** |

Of these, about 906M were used by the pipeline sessions logged in `data/inference_test/logs/sessions.csv`:

| Step | Agent | Sessions | Tokens |
|---|---|---|---|
| Step 0 | opus-5-5 | 7 | 190.6M |
| Step 1 | opus-5-5 | 21 | 381.7M |
| Step 1 | sonnet-5-5 | 16 | 333.9M |

The remaining ~97M were used in development and chat sessions.

Notes:

- About 98% of all tokens are cache reads, which are billed at a much lower rate than other tokens; output and cache creation tokens drive most of the cost.
- Claude Code deletes session transcripts after 30 days by default (`cleanupPeriodDays`), so older sessions and sessions run on other machines are not counted. The total is a lower bound.

### Environmental impact

Using an online [AI Impact Calculator](https://aiimpactcalculator.com/), this project is estimated (roughly) to have consumed a total of 14.126425 mWh. Below shows the estimate amount of other resources consumed, e.g. CO_2, water, etc:

**Data extraction using Opus 5.5**
<image src="energy_use/opus_usage.jpg"/>
<image src="energy_use/opus_perspective.jpg"/>

**Data extraction using Sonnet 5.5**
<image src="energy_use/sonnet_usage.jpg"/>
<image src="energy_use/sonnet_perspective.jpg"/>

**Development and other tasks using Opus 5.5**
<image src="energy_use/opus_usage_dev.jpg"/>
<image src="energy_use/opus_perspective_dev.jpg"/>
