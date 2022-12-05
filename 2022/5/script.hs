main = do
   input <- getContents
   let lns = lines input
   let (state, commands) = break (=="") lns

   
   let (stacks, indices) = break (== last state) state
   print stacks
