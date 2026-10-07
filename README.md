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

## Converting PDF to Markdown

Since Markdown is currently one of the better formats for LLMs to analyse, we first convert the PDFs to Markdown files. Here, I used the Python module [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) for conversion, which showed success for both text-based and image-based (scanned) PDFs.

## Data extraction with LLM

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

Additional Python scripts created by Claude as per my instructions included `check.py` to identify conflicting results between inference outputs and guidelines, `log_session.py` to log each inference session's outputs, and `usage.py` to record LLM token usage.

### Triggering the agent (draft written by Claude, edited by human)

Use 1 model per session to prevent results leakage across models during inference times. Start a fresh session for every step below. The pipeline rules are in `CLAUDE.md`, which Claude Code loads automatically; each session works out its agent from the model it runs on.

### Initial testing

1 paper that has been extracted already

The intial testing stage aimed to confirm and test that the outputs of the LLMs are consistent and follow the provided guidelines in `CLAUDE.md` while showing 0 errors when running `check.py`. 

show 1 paper -> iterate tests on 6 papers -> add 14 papers -> test

### Logging each session

Every pipeline session is logged automatically. A `SessionEnd` hook in `.claude/settings.json` runs `scripts/claude/log_session.py` when a session ends. It acts only on sessions whose prompt starts with `Run Step 0` or `Run Step 1`; other sessions are ignored. For each pipeline session it:

1. copies the session transcript (which records the model of every response) and a snapshot of the step's outputs to `data/inference_test/logs/runs/<step>_<slug>_<session id>/`: `md_opt_log.csv` and `md_opt_check.csv` for Step 0; `<slug>.csv`, `<slug>_log.csv` and `<slug>_check.csv` for Step 1;
2. adds one line to `data/inference_test/logs/sessions.csv`: date, step (`step0`, `step1-trial` or `step1`), agent, the model IDs that actually answered, Claude Code version, session ID;
3. fills the token breakdown (`n_requests`, `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`, `total_tokens`): per paper in that paper's line of the step's log, and per step as whole-session totals in `sessions.csv`. The session total minus the papers is setup, checks and wrap-up. Each request is assigned to a paper by the `started` and `finished` times the agent writes in its log. Cache-read tokens make up most of the total because every request re-reads the conversation so far; compare papers mainly on `output_tokens` and `n_requests`.

`models` in `sessions.csv` must show only the expected model ID (e.g. `claude-opus-5-5`). Any other model means the session did not run on the intended model, so its results are not valid for that agent. The agents also record the model themselves: Step 0 in the end comment of each `md_agents/` file, Step 1 in the `_run` line of `<slug>_log.csv`.

Optional: before ending a session, type `/export data/inference_test/logs/runs/<step>_<slug>_<YYYYMMDD-HHMM>.txt` to also keep the conversation as readable text.

If the hook did not run (e.g. the terminal was killed), log the session by hand; running it twice is safe:

```bash
python scripts/claude/log_session.py --session <session id>
```

**Before rerunning a step**, move that agent's live files out of the way, because papers already in the log are skipped. Their snapshot is already in `logs/runs/`. For Step 1: `data/inference_test/results/<slug>.csv`, `data/inference_test/logs/<slug>_log.csv` and `data/inference_test/logs/<slug>_check.csv`.

### Steps

1. **Step 0: optimise markdown (Opus).** Compares `data/papers_test/md/` with the PDFs in `data/papers_test/pdf_done/` and writes fixed markdown to `data/papers_test/md_agents/`.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 0 in CLAUDE.md. Do not ask questions. Stop after CHECK --step0 passes.
   ```

2. **Manual check.** Open 1–2 files in `data/papers_test/md_agents/` and compare their tables with the PDF (e.g. Kubiak 2009 Appendix 1, Benson 1985 Table 2). Step 1 is only as good as these files. Also read `data/inference_test/logs/md_opt_log.csv` for unresolved items.

3. **Step 1 trial: one paper (Opus).** New session.

   ```
   claude --model claude-opus-5-5
   ```

   ```
   Run Step 1 in CLAUDE.md. Do not ask questions. Process only "Knox & Clarke 2004 Cunninghamia_primary juvenile period", then stop.
   ```

   Check the rows in `data/inference_test/results/opus-5-5.csv`, the log in `data/inference_test/logs/opus-5-5_log.csv`, and the check report in `data/inference_test/logs/opus-5-5_check.csv`.

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

5. **Final check.** Each check exits 1 if any check fails; the reports are in `data/inference_test/logs/`.

   ```
   python scripts/claude/check.py --step0
   python scripts/claude/check.py opus-5-5
   python scripts/claude/check.py sonnet-5-5
   ```

If a session stops early (usage limit, context full), start a new session with the same prompt. Finished papers are skipped and unfinished ones are redone.

All output stays in `data/papers_test/md_agents/` and `data/inference_test/`. Nothing is written to `data/inference/` until the test run is complete.


# Token usage

optimise md: 71.3M tokens for 14 papers

data extraction: ~ slightly more than 1M tokens for both models