
import itertools
from collections.abc import Iterable


def smart_function():
    n = getattr(smart_function, '_n_call', 1)
    smart_function._n_call = n + 1
    return n


def flatten(iterable):
    """Flattens non-str iterables."""

    i = iter(iterable)

    while True:
        try:
            a = next(i)
            if isinstance(a, Iterable) and not isinstance(a, str):
                i = itertools.chain(iter(a), i)
            else:
                yield a
        except StopIteration:
            return
    # raises StopIteration anyways
    

if __name__ == "__main__":
    # Example 1
    for real_call_count in range(1, 5):
        f = smart_function
        assert f() == real_call_count

    # Example 4
    expected = [1, 2, 0, 1, 1, 2, 1, 'ab']
    actual = flatten(
        [1, 2, range(2), [[], [1], [[2]]], (x for x in [1]), 'ab']
    )
    assert expected == list(actual)

