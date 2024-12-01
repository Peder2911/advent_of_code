
import collections

if __name__ == "__main__":
    numbers = [[],[]]
    with open("data") as f:
        for line in (ln.strip().split() for ln in f.readlines()):
            for i,n in enumerate(line):
                numbers[i].append(int(n))
    
    numbers[0].sort()
    numbers[1].sort()
    dists = 0
    seen = collections.defaultdict(int)
    for i,_ in enumerate(numbers[0]):
        seen[numbers[1][i]] += 1 
        dists += abs(numbers[0][i] - numbers[1][i])
    print(f"1: {dists}")

    msum = 0
    for n in numbers[0]:
        msum += n*seen[n]
    print(f"2: {msum}")




