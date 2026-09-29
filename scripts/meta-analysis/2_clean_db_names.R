library(stringr)
library(glue)

db <- read.csv(file = "data/plants_db/apc_db_nsw_scinames.csv")

#clean up scientific names

db_clean <- db
db_clean$scientificName_clean <- NA #create a new column to store clean names

for (i in 1:nrow(db_clean)) {

    print(glue("i={i}"))

    name_split <- str_split(db_clean[i, "scientificName"], "\\s+")[[1]]
    cleanName <- character(0)

    for (j in seq_along(name_split)) {

        nameWord <- name_split[j]

        if (
            j > 1 &&
            (
                str_detect(nameWord, "[[:punct:]]") ||
                str_detect(nameWord, "^[[:upper:]]")
            )
        ) {
            break
        }

        cleanName <- c(cleanName, nameWord)
    }

    cleanName <- paste(cleanName, collapse = " ")
    print(cleanName)
    db_clean[i, "scientificName_clean"] <- cleanName

}

#sanity checks

db_clean[1, "scientificName_clean"]

#save

write.csv(db_clean, "data/plants_db/apc_db_nsw_clean.csv")
