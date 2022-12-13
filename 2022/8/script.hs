
take_while_biggest :: [Int] -> Int
take_while_biggest xs = take_while_biggest' (-1) (-1) xs 
   where
      take_while_biggest' previous cum xs'
         | previous <= (head xs') = take_while_biggest' (head xs') (cum+1) (tail xs')
         | otherwise = cum

see_from_the_left :: [[Int]] -> [(Int,Int)]

see_from_the_left matrix = indices
   where
      ys = length matrix
      xs = length (matrix !! 0)
      indices = zip (map take_while_biggest matrix) [1..ys]

numbers = map (read . (:"")) :: String -> [Int]

transpose :: [[Int]] -> [[Int]]
transpose matrix = transposed_matrix
   where
      size_x = length (matrix !! 0)
      size_y = length matrix 
      transposed_matrix = map (\xi -> map (\yi -> matrix !! yi !! xi) [(size_y-1), (size_y-2)..0]) [0..(size_x-1)] 

unique xs = unique' [] xs
   where
      unique' seen [] = seen 
      unique' seen rest = unique' seen' (tail rest) 
         where
            x = head rest
            seen' 
               | x `elem` seen = seen
               | otherwise = seen ++ [x]

set_join a b = a ++ b'
   where
      b' = filter (\x -> not $ (x `elem` a)) b

transposed_coordinates :: Int-> Int-> Int -> (Int, Int) -> (Int, Int)
transposed_coordinates size_x size_y turns coords = ((transpose_x x y), (transpose_y x y))
   where
      (x,y) = coords
      turns' = mod turns 4

      transpose_x x' y'
         | turns == 0 = x'
         | turns == 1 = size_y - y'
         | turns == 2 = size_x - x'
         | turns == 3 = y'

      transpose_y x' y'
         | turns == 0 = y'
         | turns == 1 = x' 
         | turns == 2 = size_x - x'
         | turns == 3 = size_y - y'

all_coords xs ys = foldr (\a b -> a ++ b) [] (map (\x -> map (\y -> (x,y)) [0..ys]) [0..xs])

mark_if_seen seen ys coords
   | coords `elem` seen = "x"
   | (snd coords) >= ys = "O\n"
   | otherwise = "."

main = do
   input <- getContents
   let matrix = (map numbers (lines input))
   let xs = length matrix
   let ys = length (matrix !! 0)
   let transposed_coordinates' = transposed_coordinates xs ys
   -- print matrix
   -- print (transpose (transpose matrix))
   let sides = take 4 (iterate transpose matrix)
   let all_seen = map (\(side,i) -> map (transposed_coordinates' i) (see_from_the_left side)) (zip sides [0..3])
   let unique_seen = unique $ (foldr (\a b -> a ++ b) [] all_seen)


   print(unique_seen)
   putStr ("\n" ++ (concat $ (map (mark_if_seen unique_seen ys) (all_coords xs ys))))

   -- Does not work...
