# Step 0 session log

- Date: 2026-10-02
- Agent: opus-5-5 (claude-opus-5-5), MD_AGENT
- RUN: test
- Task: run Step 0 in CLAUDE.md; stop after `CHECK --step0` passes

## Progress

```
Step 0: optimise markdown | 6 papers
[###-----------------] 1/6 (17%) Benson 1985 Cunninghamia_primary juvenile period | 11 pages
    pages 1-10 of 11 | tables rebuilt 3
    page 11 of 11 | tables rebuilt 0
    done | fixes 34 | unresolved 0
[#######-------------] 2/6 (33%) Knox & Clarke 2004 Cunninghamia_primary juvenile period | 6 pages
    pages 1-6 of 6 | tables rebuilt 2
    done | fixes 22 | unresolved 0
[##########----------] 3/6 (50%) Kubiak Cunn 2009 | 35 pages
    pages 1-10 of 35 | tables rebuilt 3
    pages 11-20 of 35 | tables rebuilt 6
    pages 21-30 of 35 | tables rebuilt 10
    pages 31-35 of 35 | tables rebuilt 5
    done | fixes 24 | unresolved 0
[#############-------] 4/6 (67%) Muir et al 2014 AustJBot_obligate seeder juvenile | 10 pages
    pages 1-10 of 10 | tables rebuilt 4
    done | fixes 28 | unresolved 0
[#################---] 5/6 (83%) Ooi 2019 JEnvManagement_fire seasonality | 8 pages
    pages 1-8 of 8 | tables rebuilt 3
    done | fixes 22 | unresolved 0
[####################] 6/6 (100%) nswfrrd_v1.3a_pdfvers_sppdata | 205 pages
    pages 1-10 of 205 | tables rebuilt 9
    pages 11-20 of 205 | tables rebuilt 10
    pages 21-30 of 205 | tables rebuilt 10
    pages 31-40 of 205 | tables rebuilt 10
    pages 41-50 of 205 | tables rebuilt 10
    pages 51-60 of 205 | tables rebuilt 10
    pages 61-70 of 205 | tables rebuilt 10
    pages 71-80 of 205 | tables rebuilt 10
    pages 81-90 of 205 | tables rebuilt 10
    pages 91-100 of 205 | tables rebuilt 10
    pages 101-110 of 205 | tables rebuilt 10
    pages 111-120 of 205 | tables rebuilt 10
    pages 121-130 of 205 | tables rebuilt 10
    pages 131-140 of 205 | tables rebuilt 10
    pages 141-150 of 205 | tables rebuilt 10
    pages 151-160 of 205 | tables rebuilt 10
    pages 161-170 of 205 | tables rebuilt 10
    pages 171-180 of 205 | tables rebuilt 10
    pages 181-190 of 205 | tables rebuilt 10
    pages 191-200 of 205 | tables rebuilt 10
    pages 201-205 of 205 | tables rebuilt 5
    done | fixes 210 | unresolved 0
Checks | Step 0 | errors 0 | warnings 0
Step 0 done | 6 optimised, 0 skipped
```

## Intermediate CHECK runs

Runs before all papers were done failed only because later papers were not processed yet:

```
check Step 0 | errors 6 | warnings 0   (after Kubiak; Muir, Ooi, nswfrrd missing)
check Step 0 | errors 4 | warnings 0   (after Muir; Ooi, nswfrrd missing)
check Step 0 | errors 2 | warnings 0   (after Ooi; nswfrrd missing)
```

Final run:

```
python scripts/claude/check.py --step0
check Step 0 | errors 0 | warnings 0 | report data/inference_test/logs/md_opt_check.csv
```

One self-caused issue was fixed during the run: the first Benson end comment contained the literal text `<br>`, which the check counts as junk. The end comment was reworded before the check ran on it.

## Summary per paper

| Paper | Pages | Tables | Fixes | Unresolved |
|---|---|---|---|---|
| Benson 1985 | 11 | 3 | 34 | none |
| Knox & Clarke 2004 | 6 | 2 | 22 | none |
| Kubiak Cunn 2009 | 35 | 4 | 24 | none |
| Muir et al 2014 | 10 | 4 | 28 | none |
| Ooi 2019 | 8 | 3 | 22 | none |
| nswfrrd_v1.3a | 205 | 204 | 210 | none |

## Methods and notes

- **Benson 1985:** scanned PDF with no text layer. Tables read from page images (Table 3 from a rotated, cropped render). Table 2 cells matched to species by vertical row position. Two Glenorie values sit between rows: 8(9) assigned to *Petrophile pulchella* and 8 to *Grevillea buxifolia*; spot-check these. Table 3 and Table 2 disagree for *Boronia ledifolia* and *Hibbertia monogyna*; both are kept as printed. *Acacia suaveolens* vicinity value printed with a dot mark is kept as 2.
- **Knox & Clarke 2004:** text-layer PDF. Page 1 order restored (title and abstract before Introduction); page breaks re-placed to match PDF pages; two HTML tables rebuilt as pipe tables.
- **Kubiak Cunn 2009:** Tables 1-3 rebuilt; Table 3 restored with all observation years. Appendix 1 (pages 15-35) rebuilt from positioned PDF text: 829 species rows, 252 exotic (matches the paper's exotic count). Underlined values (unclear whether from seed or resprout) were detected from page pixels and written as `<u>value</u>` in both the Resp and Seed columns. Bold values kept as `**bold**`. References split into one item each.
- **Muir et al 2014:** Tables 1-4 rebuilt; Gompertz equation and theta symbols restored from font-mapping junk; fitted equations and axis labels printed in Fig. 1 and Fig. 2 added; references rebuilt from PDF column text; vertical download watermark not copied.
- **Ooi 2019:** Tables 1-3 rebuilt; references rebuilt from PDF column text with soft hyphens removed; figure axis and key text added; page header, footer and page numbers added.
- **nswfrrd_v1.3a:** Excel print-out; raw markdown had no page markers; page 1 is blank. All 204 table pages rebuilt from PDF word positions, one species per row. Even pages hold regeneration and fire response reference columns, odd pages hold vital attributes, life history and habitat columns, with the same species in the same order on each page pair (2699 species rows per page type). Column headers repeated on pages that print none. PDF text colours (blue numbers, coloured VA-group letters) are not kept.

## Files written

- `data/papers_test/md_agents/*.md` (6 files, each ending with a `<!-- md_opt: ... -->` comment)
- `data/inference_test/logs/md_opt_log.csv`
- `data/inference_test/logs/md_opt_check.csv` (written by CHECK)
- This log

Nothing committed. No script files written; scratch data and image files were kept in the session scratchpad only.
