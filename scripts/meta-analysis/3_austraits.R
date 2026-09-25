library("APCalign")

apc_db <- read.csv(file = "data/plants_db/apc_db_nsw_scinames.csv", header = T)
colnames(apc_db)
apc_db["scientificName"]

create_taxonomic_update_lookup( 
  taxa = c(
    "Banksia integrifolia",
    "Acacia longifolia",
    "Commersonia rosea"
    )
)

