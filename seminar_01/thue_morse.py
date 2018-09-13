

def get_sequence_item(n):
    """"""
    res = 0
    for k in range(n):
        sz = 2 ** k
        res = (res << sz) + (~res & ((2 ** sz) - 1))
    return res


f = get_sequence_item


def get_sequence_item_recursion(n):
    if n == 0:
        return 0b0

    sz = 2 ** (n - 1)

    m = get_sequence_item_recursion(n - 1)
    return (m << sz) + (~m & ((2 ** sz) - 1))


g = get_sequence_item_recursion


if __name__ == "__main__":
    for i in range(5):
        print("%s == (%s)" % (i, bin(get_sequence_item(i))))
