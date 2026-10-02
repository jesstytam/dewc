# Meta-analysis study on primary and secondary juvenile period post-fire events

# Installation

```
git clone <this_repo>
```

# Setup

- System: Ubuntu 26.04.1 LTS
- LLM: Claude Code via the terminal
- Languages: Python, shell, R, natural language

# Data collection and cleaning

## 

# Data extraction

## Itertive improment to write CLAUDE.md

unify variables related to this study from Austraits and Fire Ecology Database.

optimise markdown output after converting PDFs to MDs running `scripts/pipeline/1_pdf2md.py`. 

test run and manual verification of answers

## Steps to trigger agents to extract data (written by Claude, edited by human)

Use 1 model per session to prevent results leakage across models during inference times. Start a fresh session for every step below. The pipeline rules are in `CLAUDE.md`, which Claude Code loads automatically; each session works out its agent from the model it runs on.

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
