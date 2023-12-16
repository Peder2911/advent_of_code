//use std::env;
use std::fs;

fn pairs(xs: &Vec<i32>) -> Vec<[i32; 2]> {
    let mut pairs: Vec<[i32; 2]> = vec![];
    let mut i = 0;
    while i < (xs.len()-1){
        let mut p: [i32; 2] = [0; 2];
        p[0] = xs[i];
        p[1] = xs[i+1];
        pairs.push(p);
        i += 1;
    }
    return pairs
}

fn diffs(xs: &Vec<i32>) -> Vec<i32> {
    return pairs(xs).iter().map(|p| p[1]-p[0]).collect()
}

fn all_zeros(xs: &Vec<i32>) -> bool {
    xs.iter().filter(|d| **d != 0).count() == 0
}

fn last<T>(xs: &Vec<T>) -> &T {
    return &xs[xs.len()-1]
}

fn print_vector_of_vectors<T:std::fmt::Display>(xss: &Vec<Vec<T>>) -> () {
    for xs in xss {
        print!("[");
        for x in xs {
            print!("{}, ",x);
        }
        print!("]\n")
    }
}

fn solve_differences(xs: &Vec<i32>) -> Vec<Vec<i32>> {
    let mut diffdiff: Vec<Vec<i32>> = vec![];
    diffdiff.push(diffs(&xs));

    while ! all_zeros(&last(&diffdiff)) {
        let next_diff = diffs(&last(&diffdiff));
        diffdiff.push(next_diff);
    }

    if last(&diffdiff).len() == 0 {
        print_vector_of_vectors(&diffdiff);
        panic!("Failed to compute diffs: Final vector was not all zeroes. The problem is unsolvable.");
    }
    return diffdiff
}

fn extrapolate(xs: &Vec<i32>) -> i32 {
    let mut diffdiff = solve_differences(&xs);
    diffdiff.reverse();
    let mut i = 0;
    while i < (diffdiff.len()-1) {
        let new_diff = last(&diffdiff[i+1]) + last(&diffdiff[i]);
        diffdiff[i+1].push(new_diff);
        i += 1;
    }
    return last(&xs) + last(&last(&diffdiff));
}

fn main(){
    let data = fs::read_to_string("./data").unwrap();
    let mut lines: Vec<Vec<i32>> = data
        .split("\n")
        .filter(|ln| ln.len() > 0)
        .map(|ln| ln
             .split(" ")
             .map(|numstr| numstr.parse::<i32>().unwrap_or(0))
             .collect())
        .collect();
    for line in lines.iter_mut() {
        line.push(extrapolate(&line));
        line.reverse();
        line.push(extrapolate(&line));
        line.reverse();
    }
    println!("Task 1: {}", lines.iter().map(|ln| last(&ln)).fold(0,|sum, x| sum + x));
    println!("Task 2: {}", lines.iter().map(|ln| ln[0]).fold(0,|sum, x| sum + x));
}
