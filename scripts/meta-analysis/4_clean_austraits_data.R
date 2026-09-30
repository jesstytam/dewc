traits <- read.csv("data/austraits/traits_nsw.csv", header = T)

traits_flowering <- subset(traits, grepl("flowering", traits$trait_name))

nrow(traits_flowering)
summary(traits_flowering)
