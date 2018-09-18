
from collections import Counter


def distribute(seq, k):
    lo, hi = min(seq), max(seq)
    d = (hi - lo) / k
    
    def bin(x):
        """Bin number."""
        if x == hi:
            return k - 1
        return int((x - lo) / d)
    
    c = Counter()
    for x in seq:
        c[bin(x)] += 1
    return [c[i] for i in range(k)]


if __name__ == "__main__":
    assert distribute([1.25, 1, 2, 1.75], 2) == [2, 2]
    assert distribute([1.25, 1, 2, 1.75], 1) == [4]
    # NOTE: For the next one, the bins are the following:
    # [1; 1.25) [1.25; 1.5) [1.5; 1.75) [1.75; 2]
    assert distribute([1.25, 1, 2, 1.75], 4) == [1, 1, 0, 2]
