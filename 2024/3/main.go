package main

import (
	"os"
	"regexp"
	"fmt"
	"strconv"
)

func runMul(match []string) int {
	x,_ := strconv.Atoi(match[1])
	y,_ := strconv.Atoi(match[2])
	//fmt.Printf("%s:\t%v\n",match[0], x * y)
	return x * y
}

func parse(program string){
	parseMul := regexp.MustCompile("^mul\\(([0-9]+),([0-9]+)\\)")
	parseDo := regexp.MustCompile("^do\\(\\)")
	parseDont := regexp.MustCompile("^don't\\(\\)")

	task1 := 0
	task2 := 0
	enabled := true
	for i,c := range []rune(program){
		if c == 'm' {
			mul := parseMul.FindStringSubmatch(program[i:])
			if mul != nil {
				result := runMul(mul)
				task1 += result
				if enabled {
					task2 += result
				}
			}
		}
		if c == 'd' {
			if do := parseDo.FindString(program[i:]); do != "" {
				enabled = true
			} else if dont := parseDont.FindString(program[i:]); dont != "" {
				enabled = false 
			}
		}
	}
	fmt.Printf("1: %v\n",task1)
	fmt.Printf("2: %v\n",task2)
}

func main(){
	dat,err := os.ReadFile("data")
	if err != nil {
		panic(err)
	}
	parse(string(dat))
}
