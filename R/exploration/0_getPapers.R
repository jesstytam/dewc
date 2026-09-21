library("stringr", help, pos = 2, lib.loc = NULL)

#load and check out the csv file

csvFile <- read.csv("data/raw/Data template for Tahnee_first draft(Juvenile period data).csv", header=T, fileEncoding="ISO-8859-1")

#get the source papers

colnames(csvFile)
sourceList <- unique(csvFile["Source"])

#remove deplicates

sub("\\s*https?://.*$", "", sourceList[5,])

sourceList_new <- sourceList

for (i in 1:nrow(sourceList_new)) {
    
    updatedEntry <- sub("\\s*https?://.*$", "", sourceList_new[i,"Source"])
    sourceList_new[i,"Source"] <- updatedEntry
}

sourceList_unique <- unique(sourceList_new["Source"])
sourceList_unique

#save

write.csv(sourceList_unique, "data/raw/source_list.csv")
