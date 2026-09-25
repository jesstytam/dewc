#load
db <- read.csv(file = "data/plants_db/APC-taxon-2026-09-25-0739.csv", header = T)

#filter for only NSW plants
db_nsw <- subset(db, taxonDistribution=="NSW")

#save
write.csv(db_nsw, "data/plants_db/apc_db_nsw.csv")
