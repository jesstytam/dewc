# A/B test: Step 1 on raw markdown

Temporary test, separate from the pipeline. It runs Step 1 on the raw `pdf2md.py` markdown (no Step 0 cleanup) for the 14 papers added on 2026-10-07, so the result can be compared with the Step 1 run on the cleaned markdown (`md_agents/`).

## For the agent running the test

Run Step 1 of `CLAUDE.md` exactly as written, with all its extraction rules, column rules (`METADATA`), CSV format and checks, but with these Setup values replaced:

```python
ROOT     = "tests/ab_raw_md/"                    # TEMPLATE, METADATA, RESULT, LOG and check reports all under ROOT
PAPERS   = "tests/ab_raw_md/papers/*.md"         # raw markdown; each file ends with an md_opt end comment, so treat it as a finished MD_OPT file
CHECK    = "tests/ab_raw_md/check_ab.py"         # same checks as scripts/claude/check.py, with the paths above; run it, never edit it
```

- `papers_sha256` = `sha256sum tests/ab_raw_md/papers/*.md | LC_ALL=C sort | sha256sum`, run from the repo root.
- Skip the check that every `MD_RAW` file has a finished `MD_OPT` file.
- Read only `tests/ab_raw_md/references/`, `tests/ab_raw_md/papers/`, `RESULT` and `LOG`. Write only `RESULT`, `LOG` and check reports under `tests/ab_raw_md/`.
- Do not read or write anything in `data/` in this session. This replaces the `CLAUDE.md` rule "Use `data/inference_test/` only" for this test.
- Do not run `scripts/claude/usage.py` or `scripts/claude/log_session.py`.

## For the user

1. Start a fresh session with Sonnet (`claude-sonnet-5-5`) and send: `Run the A/B test in tests/ab_raw_md/AB.md`. Do not start the prompt with "Run Step 1": that would make the SessionEnd hook log the session into `data/inference_test/logs/`.
2. After the session: `python tests/ab_raw_md/usage_ab.py --session <session id>` fills the token columns in `tests/ab_raw_md/logs/sonnet-5-5_log.csv`.
3. Compare: `python tests/ab_raw_md/compare.py`. Writes `tests/ab_raw_md/logs/compare_summary.csv` and `compare_details.csv`.
4. When done, delete `tests/ab_raw_md/`.

## Files

- `papers/`: raw copies of `data/papers_test/md/*.md` for the 14 papers (the 16 new papers without the duplicates `AuldScottProcFireEffectsIAWF1997-1` and `part303174`), each with the end comment `<!-- md_opt: none; raw pdf2md output, not optimised -->`.
- `references/`: copies of `data/inference_test/references/` (template.csv, metadata.csv).
- `check_ab.py`, `usage_ab.py`: thin wrappers that run `scripts/claude/check.py` and `usage.py` with the test paths.
- `compare.py`: compares the test result with the baseline Sonnet run on cleaned markdown (session e22fd76a), and measures run-to-run noise from 2 earlier Sonnet runs on the same cleaned papers.
