
import Foundation

typealias Steps = Array<Character> 
typealias Nodes = Dictionary<String, Node>

let notUpperChars = try Regex("[^A-Z]+")

struct Node {
    let left: String
    let right: String
}

struct Walker {
    var at: Node
    let steps: Array<Character> 
    private var stepIndex = 0

    mutating private func nextIndex() -> Int {
        stepIndex = (stepIndex)  - (steps.count * ((stepIndex) / steps.count))
        return stepIndex
    }

    mutating func walk(map: Nodes) {
        let instruction = steps[nextIndex()]
        if instruction == "L" {
            self.at = map[at.left]!
        } else {
            self.at = map[at.right]!
        }
    }
}


func parseNode(_ line: String) -> (String, Node) {
    let splitLine = line.split(separator:"=")
    let nodeName = splitLine[0].replacing(" ", with: "")
    let splitDescrip = splitLine[1].split(separator:",").map {$0.replacing(notUpperChars, with :"")}
    return (String(nodeName), Node(left: String(splitDescrip[0]), right: String(splitDescrip[1])))
}

func parseInput(_ data: String) -> (Steps, Nodes) {
    let lines = inputData.split(separator:"\n")
    let steps = lines[0]
    let nodes = lines[1...].map {parseNode(String($0))}
    var nodemap: Dictionary<String, Node> = [:]
    for (name, node) in nodes {
        nodemap[name] = node
    }
    return (Array(steps), nodemap)
}

func walk(from: String, instruction: Character, map: Nodes) -> String {
    let node = map[from]!
    if instruction == "L" {
        return node.left
    } else {
        return node.right
    }
}

let inputData = try! String(contentsOf:URL(fileURLWithPath:"./data"))
let (steps, nodes) = parseInput(inputData)

var atNode = "AAA"
var stepsTaken = 0
let nSteps = steps.count
while atNode != "ZZZ" {
    var stepIndex = (stepsTaken)  - (nSteps * ((stepsTaken) / nSteps))
    if stepIndex == steps.count {
        stepIndex -= steps.count
    }
    atNode = walk(from: atNode, instruction: steps[stepIndex], map: nodes)
    stepsTaken += 1
    if atNode == "ZZZ" {
        print("Arrived after \(stepsTaken) steps")
        break
    }
}
