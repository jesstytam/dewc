library("APCalign")
library("austraits")
library(glue)
library(jsonlite)

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
                                                                  "Pterostylis readii"
austraits_data$traits

traitsdb <- list()

for (i in 1:nrow(namesList)) {
  print(glue("Getting traits for {namesList[[1]][i]}"))
  traitstaxon <- tryCatch({
    extract_taxa(austraits, taxon_name = namesList[[1]][i])
  }, error = function(e) {
    traitstaxon <- NA
  })
  traitsdb <- c(traitsdb, traitstaxon)
}

traitsdb
saveRDS(traitsdb, "data/austraits/traits_nsw.RDS")

#convert rds to json

make_json_safe <- function(x) {

    if (inherits(x, "bibentry")) {
        return(as.character(x))
    }

    if (inherits(x, "traits.build")) {
        x <- unclass(x)
    }

    if (is.data.frame(x)) {
        x[] <- lapply(x, make_json_safe)
        return(x)
    }

    if (is.list(x)) {
        return(lapply(x, make_json_safe))
    }

    x
}

traitsdb_safe <- make_json_safe(traitsdb)

traitsdb_json <- toJSON(
    traitsdb_safe,
    dataframe = "rows",
    na = "null",
    auto_unbox = TRUE,
    pretty = TRUE
)

write(
    traitsdb_json,
    "data/austraits/traits_nsw.json"
)
