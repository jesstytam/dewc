# Align the taxon names of the benchmark with the Australian Plant Census (APCalign).
#
# Usage (from the repo root):
#   python scripts/claude/6_benchmark.py --taxa      # writes data/inference_test/logs/benchmark_taxa.csv
#   Rscript scripts/claude/6a_taxon_map.R            # writes data/inference_test/logs/benchmark_taxon_map.csv
#   python scripts/claude/6_benchmark.py --rescore   # scores with APC accepted names
#
# One row per name in benchmark_taxa.csv. accepted_name is empty when APCalign finds no APC accepted name
# (e.g. mosses, liverworts, phrase names). use = "yes" only for exact or punctuation-only matches; 6_benchmark.py
# compares every other name as printed.
# Fuzzy matching is off: it pairs distinct taxa (Acacia hispida -> A. hispidula); 6_benchmark.py pairs typos itself.
# Agents never read this file (logs/benchmark*.csv): it holds names from the answers.

suppressPackageStartupMessages({
  library(APCalign)
  library(dplyr)
  library(readr)
})

logs <- "data/inference_test/logs"
taxa <- read_csv(file.path(logs, "benchmark_taxa.csv"), col_types = cols(.default = "c"), na = "")

resources <- load_taxonomic_resources(quiet = TRUE)
lookup <- create_taxonomic_update_lookup(unique(taxa$name), resources = resources, quiet = TRUE,
                                         fuzzy_matches = FALSE, imprecise_fuzzy_matches = FALSE) |>
  distinct(original_name, .keep_all = TRUE) |>
  select(-genus)  # taxa has its own genus column (the benchmark key)

out <- taxa |>
  left_join(lookup, by = c(name = "original_name")) |>
  mutate(use = case_when(  # 6_benchmark.py uses rows with use = "yes"; edit by hand to override
    is.na(accepted_name) ~ "no",
    startsWith(aligned_reason, "Exact match of taxon name") ~ "yes",
    grepl("once punctuation", aligned_reason) ~ "yes",
    # first 2 words matched: only when the rest is s.lat. / s.str., not a subspecies or phrase name
    startsWith(aligned_reason, "Exact match of the first two words") & !grepl(" ", species) &
      (is.na(subsp) | grepl("^s\\.\\s?(lat|str)", subsp)) ~ "yes",
    .default = "no"
  )) |>
  select(genus, species, subsp, name, use, accepted_name, suggested_name, aligned_name,
         taxonomic_status, taxonomic_dataset, taxon_rank, aligned_reason, update_reason)

write_csv(out, file.path(logs, "benchmark_taxon_map.csv"), na = "")
cat(sprintf("written: %s | names %d | used %d | not used %d (review rows with an accepted_name and use = no)\n",
            file.path(logs, "benchmark_taxon_map.csv"), nrow(out), sum(out$use == "yes"), sum(out$use == "no")))
