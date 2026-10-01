#load
db <- read.csv(file = "data/apc/APC-taxon-2026-09-25-0739.csv", header = T)

#filter for only NSW plants
db_nsw <- subset(db, grepl("NSW", db$taxonDistribution))

write.csv(db_nsw, "data/apc/apc_db_nsw.csv", row.names=FALSE)

#remove non-scientific names
db_nsw_scinames <- subset(db_nsw, nameType=="scientific")
write.csv(db_nsw_scinames, "data/apc/apc_db_nsw_scinames.csv", row.names=FALSE)
