#
# As per usual, no imports. Long time since base R. This was fun!
# I ran this in r-base:4.2.2
#
# Seems like something was weird with the input though. One of the three-elf-groups
# actually had two items in common among them? Although this was described as not
# possible in the puzzle description. Oh well!
#

all_letters <- c(letters,LETTERS)

translate_to_value <- function(x){
   match(x, all_letters)
}

split_compartments <- function(x) {
   sack_size <- nchar(x)
   pairs <- c(
      substr(x,0,round(sack_size/2)),
      substr(x,round(sack_size/2)+1,sack_size))
}

string_to_letters <- function(x) strsplit(x, "")[[1]]

chunks <- function(x,chunk_size) {
   groups <- sort(rep_len(1:(length(x)/chunk_size), length(x)))
   split(x, groups)
}

f <- file("stdin")
open(f)
data <- readLines(f)

# Task 1
compartment_pairs <- lapply(data, split_compartments)
compartment_pairs <- lapply(compartment_pairs, function(cpts) lapply(cpts, string_to_letters))
in_both <- sapply(compartment_pairs, function(pr) intersect(pr[[1]], pr[[2]]))
print(sum(sapply(in_both, translate_to_value)))

# Task 2
groups <- chunks(data,3)
groups <- lapply(groups, function(grp) sapply(grp, string_to_letters))
group_badges <- lapply(groups, function(group) Reduce(intersect, group)[1])
print(sum(sapply(group_badges, translate_to_value)))
