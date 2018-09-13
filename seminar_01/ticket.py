

def sumdigit(x):
    """Sums the digits of a number."""
    num = x  # x // 1 ?
    res = 0
    while num:
        res, num = res + num % 10, num // 10
    return res


def is_lucky(x):
    return sumdigit(x // 1000) == sumdigit(x % 1000)


def get_nearest_lucky_ticket(n):
    """"""
    # n is a 6-digit number
    # brute force up and down, lol

    u, d = n, n
    while not (is_lucky(u) or is_lucky(d)):
        u += 1
        d -= 1
    if is_lucky(u):
        return u
    return d
