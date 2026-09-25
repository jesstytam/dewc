#load
db <- read.csv(file = "data/plants_db/APC-taxon-2026-09-25-0739.csv", header = T)

#filter for only NSW plants
db_nsw <- subset(db, taxonDistribution=="NSW")
write.csv(db_nsw, "data/plants_db/apc_db_nsw.csv")

#remove non-scientific names
db_nsw_scinames <- subset(db_nsw, nameType=="scientific")
write.csv(db_nsw_scinames, "data/plants_db/apc_db_nsw_scinames.csv")
