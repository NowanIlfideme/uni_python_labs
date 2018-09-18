
from math import log10
import logging


def width(n):
    """Width of an integer."""
    return 1 if n == 0 else int(log10(n)) + 1


def index(s, incl, k=5):
    """Finds indexes of some sort. Meh.

    Parameters
    ----------
    s : str
        String of integers.
    incl : int or tuple
        Numbers to find.
    k : int
        First numbers of 'incl' to find. Default 5.

    Returns
    -------
    found : int
        Number of inclusions.
    pos : list
        First k found positions (indexed from 1).
    """

    if isinstance(incl, int):
        incl = (incl,)

    lns = tuple(width(n) for n in incl)

    found = 0
    pos = []
    
    for i in range(len(s)):
        for j, ln in zip(incl, lns):
            if int(s[i: i + ln]) == j:
                if found < k:
                    pos.append(i + 1)
                found += 1

    if found > k:
        logging.warning(
            "Found {found} positions, "
            "showing only first {k}.".format(**locals()))
    return found, pos


if __name__ == "__main__":
    assert (1, [1]) == index('123', 1)
    assert (13, [1, 1, 2]) == index('1212122222', (1, 2, 12), 3)
