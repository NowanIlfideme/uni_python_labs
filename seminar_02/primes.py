

def get_primes(n):
    """Prime func, ptimized for even numbers."""

    if n < 2:
        return []

    return [2] + [
        z for z in range(3, n + 1, 2)
        if (z % 2 != 0) and all(
            (z % y != 0) 
            for y in range(3, int(z ** 0.5) + 1, 2)
        )
    ]


def get_primes_simple(n):
    return [
        z for z in range(2, n + 1)
        if all(
            (z % y != 0) 
            for y in range(2, int(z ** 0.5) + 1)
        )
    ]


if __name__ == "__main__":
    f = get_primes
    f(11)
