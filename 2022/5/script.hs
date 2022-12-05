alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"

restof "" = "" 
restof string = tail string

extract_indices string = fn 0 [] string
   where
      fn accumulator indices "" = indices 
      fn accumulator indices string = fn (seen + 1) (indices ++ found_index) (restof found)
         where
            (chars, found) = break (\x -> x `elem` digits) string
            seen = (length chars) + accumulator
            found_index | (found == "") = []
                        | otherwise = [seen]
            
mask indices string = map (\x -> string !! x) indices 

pivot :: [[Char]] -> [[Char]]
pivot lists = map (\x -> map (\y -> y!!x) lists') [0..((length (lists!!0) - 1))]
   where lists' = reverse lists

parse_state :: [[Char]] -> [[Char]]
parse_state state_lines = map (filter (not . (== ' '))) $ pivot $ map state_values state 
   where 
      state = take ((length state_lines)-1) state_lines
      indices = extract_indices (last state_lines)
      state_values = mask indices

mutate fn idx list = before ++ [new] ++ after
   where
      before = take idx list
      after = reverse $ take (length list - idx - 1) $ reverse list
      new = fn (list!!idx)

move_operation amount from to state = new_state'
   where
      values = take amount $ reverse (state!!from)

      new_state = mutate (\x -> x ++ values) to state
      new_state' = mutate (\x -> take ((length x)-amount) x) from new_state

parse_operation operation = move_operation amount from to
   where
      abc = map (\x -> read x :: Int) $ words $ filter (\x -> x `elem` digits ++ [' ']) operation
      amount = abc!!0
      from = (abc!!1) - 1
      to = (abc!!2) - 1

main = do
   input <- getContents
   let lns = lines input
   let (state_block, operations_block) = break (=="") lns
   let state = (parse_state state_block)
   let operations = map parse_operation (tail operations_block)
   let result = foldr (\fn st -> fn st) state operations

   print (operations_block!!1)
   print (last operations_block)

   print state 
   print result 
