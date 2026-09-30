library("APCalign")
library("austraits")
library(glue)
library(jsonlite)
library(dplyr)

#apcalign

apc_db <- read.csv(file = "data/plants_db/apc_db_nsw_clean.csv", header = T)
namesChar <- as.character(apc_db["scientificName_clean"])
namesList <- apc_db["scientificName_clean"]

apc_out <- create_taxonomic_update_lookup( 
  taxa = "Pterostylis readii"
)
apc_out

#austraits

# austraits <- load_austraits(version = "7.0.0", path = "data/austraits/test") #does not download rds file
austraits <- readRDS("data/austraits/austraits-7.0.0.rds")

austraits_data <- extract_taxa(austraits, taxon_name = "Pterostylis readii")

#get data in a loop

traitsvec <- vector("list", nrow(namesList))

for (i in seq_len(nrow(namesList))) {

    species <- namesList[[1]][i]
    print(glue("Getting traits for {species}"))

    traitstaxon <- tryCatch(
        extract_taxa(austraits, taxon_name = species),
        error = function(e) NULL
    )

    # Single brackets preserve NULL entries.
    traitsvec[i] <- list(traitstaxon)
}

#combine into a big dataframe

traits_bigtibble <- data.frame()

for (i in 1:length(traitsvec)) {
    print(glue(
        "Current iteration: {i}"
    ))
    traits_bigtibble <- bind_rows(traits_bigtibble, traitsvec[[i]]$traits)
}

#save

write.csv(traits_bigtibble, "data/austraits/traits_nsw.csv")
