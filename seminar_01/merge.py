#!/bin/env/python


def merge(A, B):
    """Merges two sorted iterables.
    
    Uses an internal generator function, which iterates over A and B.
    Also uses an internal sentinel (for weirdos who want to compare with None)
    """
    
    sentinel = object()

    return_type = type(A)

    i, j = iter(A), iter(B)

    def gen(i, j):
        a = next(i, sentinel)
        b = next(j, sentinel)
        while True:
            # Check for finished sequences
            if a is sentinel:
                while b is not sentinel:
                    yield b
                    b = next(j, sentinel)
                return
                # raise StopIteration()

            if b is sentinel:
                while a is not sentinel:
                    yield a
                    a = next(i, sentinel)
                return
                # raise StopIteration()
            
            # Do sorts
            if b < a:  # keep left-to-right sort
                yield b
                b = next(j, sentinel)
            else:  # a >= b
                yield a
                a = next(i, sentinel)
        
        # raise StopIteration() - not required
    return return_type(k for k in gen(i, j))


class Trick(object):
    """Class to trick methods that use None as a sentinel."""
    __slots__ = 'n', 
    
    def __init__(self, n):
        self.n = n

    def __lt__(self, other):
        if other is None: 
            return True
        if isinstance(other, Trick):
            return self.n < other.n
        return self.n < other

    def __gt__(self, other):
        if other is None: 
            return False
        if isinstance(other, Trick):
            return self.n > other.n
        return self.n > other

    def __repr__(self):
        return "Trick(%r)" % (self.n, )

    def __index__(self):
        return self.n


if __name__ == "__main__":

    a = [1, 2, 3, 4]
    b = [2.4, 3, 3.9, 5, 6, 10]
    c = (1., 2., 4.)
    d = ()
    e = [Trick(1), Trick(2), 3, 4, 5.5]
    f = [Trick(k) for k in b]
    g = [Trick(3), Trick(3.4), None, None]

    r1 = merge(a, b)
    r2 = merge(tuple(a), b)
    r3 = merge(tuple(a), d)
    r4 = merge(a, c)
    r5 = merge(c, a)
    r6 = merge(d, d)
    r7 = merge(c, e)
    r8 = merge(f, b)
    r9 = merge(f, g)

