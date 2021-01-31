from itertools import combinations

letters = 'zastotazel'
letters = ''.join(sorted(letters))
print(letters)

with open('paroliamo.txt', 'r') as f:
    words = [tuple(w[:-1].split(' ')) for w in f.readlines()]


def match(l):
    ret = []
    for w in words:
        if l == w[0]:
            ret.append(w[1])
    return ret


def gen(l, n):
    ret = []
    idxs = list(range(len(l)))
    combs = list(combinations(idxs, n))
    for c in combs:
        ret.append(''.join(ch for i, ch in enumerate(l) if i not in c))
    return ret


def find(l):
    acc = 0
    while len(l) - acc > 5:
        print(f'looking into matching {len(l) - acc} letters')
        candidates = gen(l, acc)
        solutions = []
        for cand in candidates:
            solutions += match(cand)
        solutions = list(dict.fromkeys(solutions))
        if solutions:
            print(solutions)
            if input('go on? (y/N): ') != 'y':
                break
            else:
                acc += 1
        else:
            acc += 1


print(find(letters))
