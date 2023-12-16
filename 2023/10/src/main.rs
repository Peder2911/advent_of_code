use std::fs;

struct Tile {
    start: bool,
    pipe: Option<Pipe>,
}

struct Coord {
    x: i32,
    y: i32
}

enum Pipe {
    UD,
    LR,
    UR,
    UL,
    DL,
    RD
}

fn parse_pipe(x: char) -> Option<Pipe> {
    match x {
        '|'=>Some(Pipe::UD),
        '-'=>Some(Pipe::LR),
        'L'=>Some(Pipe::UR),
        'J'=>Some(Pipe::UL),
        '7'=>Some(Pipe::DL),
        'F'=>Some(Pipe::RD),
        _=>None
    }
}

fn parse_tile(x: char) -> Tile {
    return Tile {
        start: x == 'S',
        pipe: parse_pipe(x),
    }
}

fn walk_from(x: i32, y: i32, data: &mut Vec<Vec<Tile>>) -> () {
}

fn find_start(data: &Vec<Vec<Tile>>) -> Option<Coord> {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    for row in data{ 
        for tile in row {
            if tile.start {
                return Some(Coord{x, y})
            }
            y += 1;
        }
        x += 1;
    }
    return None
}

fn main() {
    let data: Vec<Vec<Tile>> = fs::read_to_string("./data").unwrap().split("\n").map(|ln| ln.chars().map(parse_tile).collect()).collect();
    let start: Coord = find_start(&data).unwrap();
}
