package main

import (
	"os"
	"strings"
	"strconv"
	"slices"
	"fmt"
)

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
	seens := make(map[int]int)
	for i:=0;i<n;i++ {
		x,y := lefts[i],rights[i]
		if x > y {
			dists += x - y
		} else {
			dists += y - x
		}
		_,success := seens[y]
		if success {
			seens[y]++
		} else {
			seens[y] = 1
		}
	}
	msum := 0
	for i:=0;i<n;i++ {
		x := lefts[i]
		seen,success := seens[x]
		if !success{
			seen = 0
		}
		msum += lefts[i]*seen
	}
	fmt.Printf("1: %v\n",dists)
	fmt.Printf("2: %v\n",msum)
}
