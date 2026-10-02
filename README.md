# Meta-analysis study on primary and secondary juvenile period post-fire events

# Installation

```
git clone <this_repo>
```

# Setup

- System: Ubuntu 26.04.1 LTS
- LLM: Claude Code via the terminal
- Languages: Python, R, natural language

# Data collection and cleaning

## 

# Data extraction

## Itertive improment to write CLAUDE.md

unify variables related to this study from Austraits and Fire Ecology Database.

optimise markdown output after converting PDFs to MDs running `scripts/pipeline/1_pdf2md.py`. 

test run and manual verification of answers

### important things i included
- log files
- reference materials, e.g. metadata, 1 paper that has been extracted already
- use of code and pseudo-code for deterministic outputs
- permissions: read, write, which files or folders, etc.

## Steps to trigger agents to extract data (draft written by Claude, edited by human)

Use 1 model per session to prevent results leakage across models during inference times. Start a fresh session for every step below. The pipeline rules are in `CLAUDE.md`, which Claude Code loads automatically; each session works out its agent from the model it runs on.

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
