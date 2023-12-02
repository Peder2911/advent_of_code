package main
import (
   "fmt"
   "strings"
   "strconv"
   "os"
   "bufio"
)
type configuration struct {
   Red int
   Green int
   Blue int
}

type round struct {
   Red int
   Green int
   Blue int
}

func (r round) String() string {
   return fmt.Sprintf("{Red: %v Green %v Blue %v}", r.Red, r.Green, r.Blue)
}

type game struct {
   Id int
   Rounds []round
}

func (g game) String() string {
   return fmt.Sprintf("Game %v: %v", g.Id, g.Rounds)
}

func (g *game) valid_with(config configuration) bool{
   valid := true
   for _,round := range(g.Rounds) {
      valid = valid && (round.Red <= config.Red && round.Green <= config.Green && round.Blue <= config.Blue)
   }
   return valid
}

func parse_game(input string) game {
   game := game{}
   parsed_input := strings.Split(input, ":")
   gameinfo := parsed_input[0]
   rounds := parsed_input[1]

   parsed_gameinfo := strings.Split(gameinfo, " ")
   game_id, err := strconv.Atoi(parsed_gameinfo[1])
   if err != nil {
      panic(fmt.Sprintf("Failed to parse game info %s", gameinfo))
   }
   game.Id = game_id

   for _,roundstring := range(strings.Split(rounds,";")) {
      round := round{}
      for _,play := range(strings.Split(roundstring,",")){
         parsed_play := strings.Split(strings.TrimSpace(play), " ")
         number,err := strconv.Atoi(parsed_play[0])
         if err != nil {
            panic(fmt.Sprintf("Failed to parse play: %s: %s", parsed_play[0], err))
         }

         color := parsed_play[1]
         switch color {
            case "red":
               round.Red = number
            case "green":
               round.Green = number
            case "blue":
               round.Blue = number
         }
      }

      game.Rounds = append(game.Rounds, round)
   }

   return game
}

func intmax(a int, b int) int {
   if a > b {
      return a
   }
   return b
}

func (g *game) minimum_viable_config() configuration {
   config := configuration{}
   for _,round := range(g.Rounds) {
      config.Red = intmax(config.Red, round.Red)
      config.Green = intmax(config.Green, round.Green)
      config.Blue = intmax(config.Blue, round.Blue)
   }
   return config
}

func (c *configuration) power() int {
   return c.Red * c.Green * c.Blue
}

func main(){
   file, err := os.Open("data")
   if err != nil {
      panic("Failed to open data file")
   }
   defer file.Close()
   scanner := bufio.NewScanner(file)

   config := configuration{Red: 12, Green: 13, Blue: 14}
   games := []game{}
   for scanner.Scan() {
      games = append(games, parse_game(scanner.Text()))
   }

   task_one := 0
   task_two := 0
   for _,game := range(games) {
      if game.valid_with(config) {
         task_one = task_one + game.Id
      }
      minimum_viable_config := game.minimum_viable_config()
      task_two = task_two + minimum_viable_config.power()
   }
   fmt.Printf("Task one: %v\n", task_one)
   fmt.Printf("Task two : %v\n", task_two)
}
