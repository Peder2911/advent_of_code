package main
import (
   "fmt"
   "strings"
   "strconv"
   "os"
   "bufio"
   "log"
   "math"
)

type MappingRange struct {
   source int
   dest int
   n int
}

func parse_input_mapping_range(input string) (*MappingRange, error) {
   var err error
   parts := strings.SplitN(input, " ", 3)
   imr := MappingRange{}
   imr.dest, err = strconv.Atoi(parts[0])
   imr.source, err = strconv.Atoi(parts[1])
   imr.n, err = strconv.Atoi(parts[2])
   if err != nil {
      return nil, fmt.Errorf("Failed to parse input mapping range: %s", err)
   }
   return &imr, nil
}

type Almanac struct {
   mappings[7][]*MappingRange
}

func parse_almanac(lines []string) (*Almanac, error) {
   id := Almanac{}
   i := -1 
   for _,ln := range lines {
      if ln != "" {
         if ln[len(ln)-4:] == "map:"{
            i++
         } else {
            imr, err := parse_input_mapping_range(ln)
            if err != nil {
               return nil, fmt.Errorf("Bad input: %s", err)
            }
            id.mappings[i] = append(id.mappings[i], imr)
         }
      }
   }
   return &id, nil
}

func (a *Almanac) seed_to_location(seed int) int {
   val := seed
   for _,mapping_type := range a.mappings {
      maps_to := -1 
      for _,mapping := range mapping_type {
         if(val >= mapping.source && val < mapping.source + mapping.n){
            offset := val - mapping.source
            maps_to = mapping.dest + offset
            fmt.Printf("\t%v\t->\t\t%v\n", val, maps_to)
            val = maps_to
            break 
         }
      }
      if maps_to < 0{ 
         fmt.Printf("\t%v\t->\t\t%v (identical)\n", val, val)
      }
   }
   return val
}

type seeds []int

func parse_seed_list(input string) (*seeds, error) {
   seeds := seeds{}
   for _,ss := range strings.Split(input[7:], " "){
      s,err := strconv.Atoi(ss)
      if err != nil {
         return nil, err
      }
      seeds = append(seeds, s)
   }
   return &seeds, nil
}

func imin(a int,b int) int{
   if a < b{
      return a
   }
   return b
}

func main(){
   file, err := os.Open("data")
   if err != nil {
      panic(fmt.Sprintf("Failed to open input file: %s", err))
   }
   defer file.Close()
   scanner := bufio.NewScanner(file)

   log.Println("Parsing seed list...")
   scanner.Scan()
   seeds_line := scanner.Text()
   seeds,err := parse_seed_list(seeds_line)
   if err != nil {
      panic(fmt.Sprintf("Failed to parse seed list: %s", err))
   }
   log.Println(fmt.Sprintf("Has %v seeds", len(*seeds)))
   var lines []string
   for scanner.Scan() {
      lines = append(lines, scanner.Text())
   }
   almanac,err := parse_almanac(lines)
   if err != nil {
      panic(fmt.Sprintf("Failed to parse input data: %s", err))
   }
   var locations []int
   var smallest_location int = math.MaxInt 
   for _, seed := range *seeds {
      location := almanac.seed_to_location(seed)
      smallest_location = imin(location, smallest_location)
      locations = append(locations, location)
      fmt.Println(fmt.Sprintf("Seed:\t%v\tLocation:\t%v", seed, location))
   }
   fmt.Printf("Task 1:\t\t\t\t\t%v\n", smallest_location)
}
