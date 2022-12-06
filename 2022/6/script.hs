marker mem cond seq = marker' (mem+1) init_mem init_seq 
   where
      marker' :: Int -> [Char] -> [Char] -> Int
      marker' acc prev [] = -1 
      marker' acc prev xs 
         | (cond ((tail prev) ++ (take 1 xs))) = acc
         | otherwise = marker' (acc+1) ((tail prev) ++ [head xs]) (tail xs)

      (init_mem, init_seq) = splitAt mem seq

unique seq = unique' [] seq
   where
      unique' seen [] = seen
      unique' seen seq' = unique' seen' xs
         where
            (x,xs) = splitAt 1 seq'
            seen' 
               | not $ (x `elem` seen) = seen ++ [x]
               | otherwise = seen

all_unique xs = (length (unique xs)) == (length xs)

main = do
   input <- getContents
   let start_of_packet = marker 4 all_unique
   let start_of_message = marker 14 all_unique

   print (start_of_packet input)
   print (start_of_message input)
