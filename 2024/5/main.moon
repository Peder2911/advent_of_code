
contains = (xs, y) ->
   for _,x in pairs xs
      if x == y
         return true
   return false


orderings = {}
series = {}
scanning_orderings = true

for line in io.lines "data"
   if scanning_orderings
      if line == ""
         scanning_orderings = false
         continue
      l,r = string.match(line, "(%d+)|(%d+)")
      if l != nil
         if orderings[l]
            table.insert(orderings[l], r)
         else
            orderings[l] = { r }
   else
      xs = {}
      for x in string.gmatch(line, "%d+")
         table.insert(xs,x)
      table.insert(series,xs)

answer = 0
for _,xs in pairs series
   legal = true
   seen = {}
   mid = math.floor(table.getn(xs) / 2)+1
   for i,x in pairs xs
      if orderings[x]
         for prev in *xs[,i]
            if contains(orderings[x],prev)
               legal = false
      if not legal
         break

   if legal
      answer = answer + xs[mid]

print(string.format("Task 1: %i", answer))
