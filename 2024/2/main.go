package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Window [3]*int

func (w Window) Rtrend() int {
	if w[2] == nil {
		return 0 
	}
	return *w[2] - *w[1]
}

type TimeSeries []int

func ParseTimeSeries(line string) TimeSeries {
	numbers := strings.Split(line," ")
	timeSeries := make(TimeSeries, len(numbers))
	for i,n := range numbers {
		x,err := strconv.Atoi(n)
		if err != nil {
			panic(err)
		}
		timeSeries[i] = x
	}
	return timeSeries
}

func (ts *TimeSeries) SafetyLevel() int {
	tsDirection := 0
	wDirection := 0
	safetyLevel := 0
	for _,window := range ts.Windows() {
		// Ignore tail window
		if window[2] == nil {
			break
		}
		
		// Check magnitude
		trend := window.Rtrend()
		if trend == 0 || trend > 3 || trend < -3 {
			safetyLevel --
			continue
		}

		// Check same direction
		if trend > 0 {
			wDirection = 1
		} else if trend < 0 {
			wDirection = -1
		}
		if tsDirection == 0 {
			tsDirection = wDirection
		} else {
			if wDirection != tsDirection {
				safetyLevel --
			}
		}
	}
	return safetyLevel 
}

func (ts TimeSeries) Windows() []Window {
	windows := make([]Window, len(ts))
	for i:=0;i<len(ts);i++ {
		if i == 0 {
			windows[i] = Window{nil, &ts[i], &ts[i+1]}
			continue
		}
		if i == (len(ts)-1) {
			windows[i] = Window{&ts[i], &ts[i], nil}
			break
			
		}
		windows[i] = Window{&ts[i-1], &ts[i], &ts[i+1]}
	}
	return windows
}

func (ts TimeSeries) String() string {
	return fmt.Sprintf("TimeSeries{%s}", fmt.Sprint([]int(ts)))
}

type TimeSeriesSeries []TimeSeries

func ParseTimeSeriesSeries(data string) *TimeSeriesSeries {
	lines := strings.Split(strings.Trim(string(data)," "),"\n")
	tss := make(TimeSeriesSeries,0)
	for _,s := range lines {
		if s != "" {
			tss = append(tss, ParseTimeSeries(s))
		}
	}
	return &tss
}

func (tss TimeSeriesSeries) Report() *TimeSeriesSeriesReport {
	report := TimeSeriesSeriesReport{}
	for _,ts := range tss {
		level := ts.SafetyLevel()
		if level == 0 {
			report.StrictlySafeSeries++
		}
		if level == -1 {
			report.KindOfSafeSeries++
		}
	}
	return &report
}

type TimeSeriesSeriesReport struct {
	StrictlySafeSeries int
	KindOfSafeSeries int
}

func (tssr TimeSeriesSeriesReport) String() string {
	return fmt.Sprintf("Series contained %v (%v damp.) safe time series.", tssr.StrictlySafeSeries, tssr.KindOfSafeSeries)
}

func main(){
	dat,err := os.ReadFile("data")
	if err != nil {
		panic(err)
	}
	tss := ParseTimeSeriesSeries(string(dat))
	for _,ts := range *tss {
		fmt.Printf("%v: %v\n",ts, ts.SafetyLevel())
	}
	fmt.Print(tss.Report())
}
