package main
import (
   "os"
   "bufio"
   "fmt"
   "strings"
   "strconv"
   "regexp"
)

type Miliseconds int
func (m Miliseconds) String() string{
   return fmt.Sprintf("%v ms", int(m))
}
type Milimeters int
func (m Milimeters) String() string{
   return fmt.Sprintf("%v mm", int(m))
}
type MilimetersPerMiliseconds int
func (m MilimetersPerMiliseconds) String() string{
   return fmt.Sprintf("%v mm/ms", int(m))
}

type Race struct {
   Time Miliseconds 
   Record Milimeters 
}
func (r Race) String() string{
   return fmt.Sprintf("Race{time: %s, record: %s}", r.Time, r.Record)
}


type Attempt struct {
   ButtonTime Miliseconds
   DistanceTravelled Milimeters
   *Race
}

func (a Attempt) String() string {
   return fmt.Sprintf(
      "Attempt{%v, buttontime: %s, distance: %s, breaks_record: %v}",
      a.Race, a.ButtonTime, a.DistanceTravelled, a.RecordBreaking(),
   )
}

func Travel(time Miliseconds, velocity MilimetersPerMiliseconds) Milimeters{
   return Milimeters(int(time) * int(velocity))
}

func (r *Race) attempt(buttontime Miliseconds) Attempt {
   time_to_race := r.Time - buttontime
   speed := MilimetersPerMiliseconds(buttontime)
   return Attempt{
      ButtonTime: buttontime,
      DistanceTravelled: Travel(time_to_race, speed),
      Race: r,
   }
}

func (r *Race) PossibleAttempts() []Attempt {
   var attempts []Attempt
   for i := Miliseconds(0); i < r.Time; i++ {
      attempt := r.attempt(i)
      attempts = append(attempts, attempt)
   }
   return attempts
}

func (a *Attempt) RecordBreaking() bool { 
   return a.DistanceTravelled > a.Record
}

func (r *Race) PossibleRecords() int {
   var result = 0
   for _, attempt := range r.PossibleAttempts() {
      if attempt.RecordBreaking() {
         result ++
      }
   }
   return result
}

type InputData [2][4]int

var multiple_spaces = regexp.MustCompile(" +")

func ParseLine(ln string) (*[4]int,error) {
   var result[4]int
   entries := strings.SplitN(multiple_spaces.ReplaceAllString(ln, " ")," ", 5)
   for i:=0; i<4; i++ {
      num,err := strconv.Atoi(entries[i+1])
      if err != nil {
         return nil, err
      }
      result[i] = num
   }
   return &result, nil
}

func ReadInput(fname string) (*[2][4]int, error) {
   f,err := os.Open("data")
   if err != nil {
      return nil, err
   }
   scan := bufio.NewScanner(f)
   scan.Scan()
   times,err := ParseLine(scan.Text())
   if err != nil {
      return nil, err
   }
   scan.Scan()
   distances,err := ParseLine(scan.Text())
   if err != nil {
      return nil, err
   }
   return &[2][4]int{*times, *distances}, nil
}

func ReadBadlyKernedInput(fname string) (*Race, error) {
   f,err := os.Open("data")
   if err != nil {
      return nil, err
   }
   scan := bufio.NewScanner(f)
   scan.Scan()
   time,err := strconv.Atoi(strings.Join(strings.Split(multiple_spaces.ReplaceAllString(scan.Text()," ")," ")[1:],""))
   if err != nil {
      return nil, err
   }
   scan.Scan()
   distance,err := strconv.Atoi(strings.Join(strings.Split(multiple_spaces.ReplaceAllString(scan.Text()," ")," ")[1:],""))
   if err != nil {
      return nil, err
   }
   return &Race{Time:Miliseconds(time), Record:Milimeters(distance)},nil
}

func InputAsRaces(input InputData) [4]Race {
   var result [4]Race
   for i := 0; i < 4; i++ {
      result[i] = Race{
         Time: Miliseconds(input[0][i]), 
         Record: Milimeters(input[1][i]),
      }
   }
   return result
}

func TaskOne(races [4]Race) int{
   var result int = 0
   for _,race := range races {
      possible_records := race.PossibleRecords()
      if result == 0 {
         result = possible_records 
      } else {
         result = result * possible_records
      }
   }
   return result
}

func main(){
   task_one_data,err := ReadInput("data")
   if err != nil {
      panic(fmt.Sprintf("Failed to read input data: %s", err))
   }
   races := InputAsRaces(*task_one_data)
   fmt.Printf("Task one: %v\n", TaskOne(races))

   task_two_race,err := ReadBadlyKernedInput("data")
   fmt.Printf("Task two: %v\n", task_two_race.PossibleRecords())
}
