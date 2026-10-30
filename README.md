# Meta-analysis study on primary and secondary juvenile period post-fire events

# Installation

```
git clone <this_repo>
cd <this_repo>
pip install -r requirements.txt
```

# My system's setup

- System: Ubuntu 26.04.1 LTS
- LLM: Claude Code via the terminal
- Languages: Python, shell/bash script, R, natural language

# Data collection

tbd

# Data cleaning

<!-- ![](assets/pipeline_flowchart.drawio.pdf) -->
<image src="assets/pipeline_flowchart.drawio.pdf"/>

## Converting PDF to Markdown

Since Markdown is currently one of the better formats for LLMs to analyse, we first convert the PDFs to Markdown files. Here, I used the Python module [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) for conversion, which showed success for both text-based and image-based (scanned) PDFs.

# Data extraction with LLM

## Important considerations

Since Claude / LLM is responsible for data extraction, the pipeline instructions were create through a back-and-fourth conversation with the chatbot. This was done by first having a simple outline of the requirements, including the following:

- input and output formats
- log files, what to log, e.g. token usage and terminal outputs
- reference materials, e.g. metadata
- language requirements, i.e. use of code and pseudo-code for deterministic outputs
- read and write permissions for which files and folders

## Writing CLAUDE.md

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

## Triggering the agent (draft written by Claude, edited by human)

Use 1 model per session to prevent results leakage across models during inference times. Start a fresh session for every step below. The pipeline rules are in `CLAUDE.md`, which Claude Code loads automatically; each session works out its agent from the model it runs on.

## Initial testing

The intial testing stage aimed to confirm and test that the outputs of the LLMs are consistent and follow the provided guidelines in `CLAUDE.md` while showing 0 errors when running `4a_check.py`. 

I first provided 1 paper that has been extracted already as an example. I then provided 6 papers that required extraction 



show 1 paper -> iterate tests on 6 papers -> add 14 papers -> test

## Logging each session

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

## Steps

1. **Step 0: optimise markdown (Opus).** Works through `data/papers_test/md_raw/`: text-layer papers are moved unchanged to `data/papers_test/md_llm/`; scanned papers are compared with their PDF in `data/papers_test/pdf_clean/`, fixed, and written to `data/papers_test/md_llm/`. `md_raw/` is empty when Step 0 is done.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 0 in CLAUDE.md. Do not ask questions. Stop after CHECK --step0 passes.
   ```

2. **Manual check.** Open 1–2 files in `data/papers_test/md_llm/` and compare their tables with the PDF (e.g. Kubiak 2009 Appendix 1, Benson 1985 Table 2). Step 1 is only as good as these files. Also read `data/inference_test/logs/md_opt_log.csv` for unresolved items.

3. **Step 1 trial: one paper (Opus).** New session.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions. Process only "Knox & Clarke 2004 Cunninghamia_primary juvenile period", then stop.
   ```

   Check the rows in `data/inference_test/results/opus-5-5_raw.csv` (values as printed in the paper), the log in `data/inference_test/logs/opus-5-5_log.csv`, and the check report in `data/inference_test/logs/opus-5-5_check.csv`.

4a. **Step 1: all papers (Opus).** New session. Papers already in the log are skipped.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions. Stop after the final CHECK run.
   ```

4b. **Step 1: all papers (Sonnet).** New session, same prompt.

   ```
   claude --model claude-sonnet-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions. Stop after the final CHECK run.
   ```

5. **Normalise.** Converts the raw results (values as printed) into the final results: time values (value + `<column>_unit` cells) to each column's unit, `pjp_mths`, case, dashes, `scientific_name` and `pdf_path`. Writes `data/inference_test/results/<slug>.csv`; the raw file is not changed. Rerun it after any change to the script; no re-extraction needed.

   ```
   python scripts/pipeline/5_normalise.py opus-5-5 sonnet-5-5
   ```

6. **Final check.** Each check exits 1 if any check fails; the reports are in `data/inference_test/logs/` (`<slug>_check.csv` for raw, `<slug>_check_final.csv` for final).

   ```
   python scripts/claude/4a_check.py --step0
   python scripts/claude/4a_check.py opus-5-5
   python scripts/claude/4a_check.py sonnet-5-5
   python scripts/claude/4a_check.py opus-5-5 --final
   python scripts/claude/4a_check.py sonnet-5-5 --final
   ```

If a session stops early (usage limit, context full), start a new session with the same prompt. Finished papers are skipped and unfinished ones are redone.

All output stays in `data/papers_test/md_llm/` and `data/inference_test/`. Nothing is written to `data/inference/` until the test run is complete.


# Token usage

optimise md: 0.5-15M tokens per paper

data extraction: ~ slightly more than 1M tokens for both models

# Benchmarking

I spent a good few weeks thinking about how to benchmark the extraction results against the ground truth, using methods such as F1 and Levenshtein distance. However, after more thinking, I realised that since 100% accuracy is only a theoretical number, as even a human produces around 4-5% error rates, there is no need to optimise the model(s) any further (currently at ~80% accurate). The biggest time lag in this pipeline can be cut even shorter if I can somehow reduce the time taken for a human to review the extraction results.

# Human-in-the-loop GUI

This is the part where I highlight my creation of an application that can increase the speed at which extraction results can be checked. 

# Adapting Claude for meta-analysis

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
