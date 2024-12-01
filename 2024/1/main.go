package main

import (
	"os"
	"strings"
	"strconv"
	"slices"
	"fmt"
)

type intcounter map[int]int

func (i intcounter) Count(n int) {
	_,success := i[n]
	if success {
		i[n]++
	} else {
		i[n] = 1
	}
}

func main(){
	dat,_ := os.ReadFile("data")
	lines := strings.Split(string(dat),"\n")
	n := len(lines)
	lefts := make([]int,n)
	rights := make([]int,n)
	for i,line := range(lines) {
		if line != "" {
			numbers := strings.Split(line,"   ")
			lefts[i],_ = strconv.Atoi(numbers[0])
			rights[i],_ = strconv.Atoi(numbers[1])
		}
	}
	slices.Sort(lefts)
	slices.Sort(rights)
	dists := 0
	leftCounts := intcounter{}
	rightCounts := intcounter{}
	for i:=0;i<n;i++ {
		x,y := lefts[i],rights[i]
		if x > y {
			dists += x - y
		} else {
			dists += y - x
		}
		leftCounts.Count(lefts[i])
		rightCounts.Count(rights[i])
	}

	csum := 0
	for number,leftCount := range leftCounts {
		csum += (leftCount * (number*rightCounts[number]))
	}

	fmt.Printf("1: %v\n",dists)
	fmt.Printf("2: %v\n",csum)
}
