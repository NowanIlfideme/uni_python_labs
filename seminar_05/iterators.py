
import functools
# import itertools


def transpose(it):
    """Returns transpose of 2D iterable."""
    return zip(*it)


def scalar_product(a, b):
    """Returns scalar product of two iterables."""

    def clean(el):
        return el if isinstance(el, (int, float)) else int(el)

    try:
        return sum(clean(x) * clean(y) for x, y in zip(a, b))
    except ValueError:
        return None


def scalar_product_alt(a, b):
    """Returns scalar product of two iterables.
    
    This doesn't have even a list comprehension."""

    def clean(el):
        return el if isinstance(el, (int, float)) else int(el)

    def cm(sm, xy):
        return sm + (clean(xy[0]) * clean(xy[1]))

    try:
        return functools.reduce(cm, zip(a, b), 0)
    except ValueError:
        return None


if __name__ == "__main__":

    # Example 2
    # TEST transpose    
    def tst_2(expected, arg):
        actual = transpose(z for z in arg)
        assert expected == list(map(list, actual))

    tst_2([[1, 2], [-1, 3]], [[1, -1], [2, 3]])
    tst_2([[1, 2, 3], [-1, 3, 4]], [[1, -1], [2, 3], [3, 4]])

    # Example 3
    assert scalar_product([1., '2'], [-1, 1]) == 1
    assert scalar_product([1., 'abc'], [-1, 1]) is None

    assert scalar_product_alt([1., '2'], [-1, 1]) == 1
    assert scalar_product_alt([1., 'abc'], [-1, 1]) is None
