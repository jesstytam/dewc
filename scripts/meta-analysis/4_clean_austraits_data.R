traits <- read.csv("data/austraits/traits_nsw.csv", header = T)

traits_flowering <- subset(traits, grepl("flowering", traits$trait_name))
write.csv(traits_flowering, "data/austraits/traits_nsw_flowering.csv", row.names=FALSE)

nrow(traits_flowering)
summary(traits_flowering)

