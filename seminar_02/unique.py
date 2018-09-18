
from collections import Counter


def compress(p):
    c = Counter()
    for n in p:
        c[n] += 1
    res = [z for z in c.items()]
    return res


if __name__ == "__main__":
    expected_sorted = [(1, 2), (2, 1)]
    actual_sorted = sorted(compress([1, 2, 1]))
