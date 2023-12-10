import Foundation

typealias Bet = Int

typealias Card = Character 

typealias Hand = Array<Character>

enum HandType: Int {
    case HighCard = 1
    case OnePair
    case TwoPair
    case ThreeOfAKind
    case FullHouse
    case FourOfAKind
    case FiveOfAKind
}

struct Play {
    let hand: Hand
    let bet: Bet
    func type(joker: Bool = false) -> HandType {
        var seen = count(values:hand)
        var jokers = 0
        if joker {
            jokers = seen["J"] ?? 0
            seen["J"] = 0

            var giveJokers: Character? = nil
            var highest = 0
            for (k,v) in seen {
                if v > highest {
                    giveJokers = k
                    highest = max(highest,v)
                }
            }
            if giveJokers != nil {
                seen[giveJokers!]! += jokers
            }
        }

        if seen.values.contains(5) {
            return HandType.FiveOfAKind
        }
        if seen.values.contains(4) {
            return HandType.FourOfAKind
        }
        if seen.values.contains(3) {
            if seen.values.contains(2) {
                return HandType.FullHouse
            } else {
                return HandType.ThreeOfAKind
            }
        }
        if seen.values.contains(2) {
            let counts = count(values:Array(seen.values))
            let twos = counts[2] ?? 1
            if twos == 1 {
                return HandType.OnePair
            } else {
                return HandType.TwoPair
            }
        }
        return HandType.HighCard
    }

    func compareCards(_ other: Play, joker: Bool = false) -> Bool {
        for c in 0...5 {
            if hand[c] != other.hand[c] {
                return cardValue(hand[c], joker: joker)! > cardValue(other.hand[c], joker: joker)!
            }
        }
        fatalError("Failed to compare hands: \(self) vs. \(other)")
    }

    func compare(_ other: Play, joker: Bool = false) -> Bool {
        let aType: HandType = type(joker:joker)
        let bType: HandType = other.type(joker:joker)
        if aType == bType {
            return compareCards(other, joker:joker)
        } else {
            return  aType.rawValue > bType.rawValue
        }
    }
}

let cardStrengths: Dictionary<Character, Int> = [
    "2":1,
    "3":2,
    "4":3,
    "5":4,
    "6":5,
    "7":6,
    "8":7,
    "9":8,
    "T":9,
    "J":10,
    "Q":11,
    "K":12,
    "A":13
]

func cardValue(_ card: Card, joker: Bool = false) -> Int? {
    if joker && card == "J" {
        return 0
    }
    return cardStrengths[card]
}

func count<T>(values: Array<T>) -> Dictionary<T, Int> {
    var counts: Dictionary<T, Int> = [:]
    for value in values {
        if counts[value] != nil {
            counts[value]! += 1
        } else {
            counts[value] = 1
        }
    }
    return counts
}

func calculateScore(_ plays: Array<Play>) -> Int {
    var score = 0
    var rank: Int
    for (i, play) in zip(0...plays.count, plays) {
        rank  = plays.count - i 
        score += (rank * play.bet)
    }
    return score
}

func parseInput(_ data: String) -> Array<Play> {
    return data.split(separator: "\n").map {
    let splitLine = $0.split(separator: " ")
    let hand = Array(splitLine[0])
    let bet = Int(splitLine[1])!
    return Play(hand: hand, bet: bet)
}
}

func main() {
    let path = URL(fileURLWithPath:"./data")
    let data = try! String(contentsOf:path) 

    var plays = parseInput(data)

    plays.sort {$0.compare($1)}
    print("Task 1: \(calculateScore(plays))")

    plays.sort {$0.compare($1, joker: true)}
    print("Task 2: \(calculateScore(plays))")
}

main()
