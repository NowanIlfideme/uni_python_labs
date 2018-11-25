
from numbers import Integral
from collections.abc import Iterable
from copy import copy as shallowcopy  # , deepcopy
# import itertools


class MidSkipQueue(object):
    """Holds only first k and last k elements. Why? IDK.
    
    This is a leaky collection without removable elements.
    """

    def __init__(self, k, iterable=()):
        # Arg checking
        assert isinstance(k, Integral) and k >= 0
        assert isinstance(iterable, Iterable)
        k = int(k)
        self.k = k

        # Save elements

        # NOTE: The following works, but not quite
        # Fails if len(it) < 2*k
        # self._front = list(itertools.islice(it, k))
        # self._rear = collections.deque(iterable, maxlen=k)

        front = []
        rear = []

        cnt = 0
        it = iter(iterable)
        try:
            while True:
                el = next(it)
                if cnt < k:
                    front.append(el)
                elif cnt < 2 * k:
                    # start filling rear
                    rear.append(el)
                else:  # cnt >= 2 * k
                    # overwrite elements
                    rear[cnt % k] = el
                cnt += 1
        except StopIteration:
            pass
        self._rear = rear[cnt % k:] + rear[: cnt % k]
        self._front = front

    def clone(self):
        """Returns a shallow copy of self."""
        res = self.__class__(
            self.k, 
            self._front + self._rear  # Returns a copy, so OK
        )
        return res

    def __str__(self):
        # TODO: convert to string
        # For large k, limit the input (like pandas)

        kmax = 5
        mdl = ", ".join(
            [str(x) for x in self._front[:kmax]] + 
            ["..."] +
            [str(x) for x in (self._rear[-kmax:])]
        )
        return "[%s]" % mdl

    def __repr__(self):
        if len(self) <= self.k:
            snd = repr(self._front + self._rear)
        else:
            snd = "[%s, ..., %s]" % (
                ", ".join(repr(k) for k in self._front),
                ", ".join(repr(k) for k in self._rear),            
            )

        return "%s(%r, %s)" % (
            self.__class__.__name__, self.k, snd
        )

    def __eq__(self, other):
        # Equality for queues - same elements
        return (
            (self.k == other.k) and
            all(a == b for a, b in zip(self, other))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    class _Iterator(object):
        def __init__(self, msq):
            self.msq = msq
            self.i = 0

        def __next__(self):
            try:
                res = self.msq[self.i]
            except (IndexError, AssertionError):
                raise StopIteration
            self.i += 1
            return res

    def __iter__(self):
        return MidSkipQueue._Iterator(self)

    def __len__(self):
        return len(self._front) + len(self._rear)

    def __getitem__(self, idx):
    
        # Also allow slices
        if isinstance(idx, slice):
            # This is the lazy version: 
            return self.__class__(self.k, list(self)[idx])
            # It works fine, probably too slow


        # For non-slice indexes
        # return list(self)[idx]  # The lazy version :P

        idx = int(idx)
        if idx < 0:
            idx += len(self)
        assert (idx < len(self) and idx >= 0)

        # Get the element 
        if idx < self.k:
            return self._front[idx]
        return self._rear[idx - self.k]

    def index(self, obj):
        """Finds index of obj in self (or -1 if nonexistant)."""
        
        try:
            idx = self._front.index(obj)
            return idx
        except ValueError:
            pass
        
        try:
            idx = self._rear.index(obj)
            return idx + len(self._front)
        except ValueError:
            pass

        # we really should raise ValueError to get proper
        # behavior, but the spec says "return -1" so OK
        return -1

    def __contains__(self, obj):
        # This is the 'obj in self' operator
        return (obj in self._front) or (obj in self._rear)

    def append(self, *objs):
        """Appends one or more objects to this collection."""

        # "Try to make this operation O(1) amortized"
        # ...
        # That means I'd have to redo everything. :(

        if len(self._front) < self.k:
            # Take possible elems from objs and fit to front
            f_el = (self.k - len(self._front))
            self._front.extend(
                objs[:f_el]
            )
            objs = objs[f_el:]
        
        # 
        objs = objs[-self.k:]
        self._rear[-len(objs):] = objs

    def __add__(self, iterable):
        # TODO: add another iterable
        res = self.clone()
        res.append(*list(iterable))
        return res


#

if __name__ == "__main__":
    # Test 1
    q = MidSkipQueue(1) 
    q.append(-1)  # q: [-1]
    q += (-2, -3)  # q: [-1, -3] - the first and the last remain
    assert list(q) == [-1, -3] 
    q.append(4)  # q: [-1, 4] - the last item has been replaced
    assert list(q) == [-1, 4] 
    assert q[-1] == 4 

    # Test 2
    q2 = MidSkipQueue(2, [1, 2, 3, 4, 5]) 
    q2b = q2 + [-1, 7] 
    assert (5 not in q2b) 
    assert list(q2b) == [1, 2, -1, 7] 
    assert q2.index(4) == 2 
    assert q2.index(3) == -1  # not in q2, funnily enough
    assert list(MidSkipQueue(1, q2)) == [1, 5] 
    assert (q2b == q2 + q + [7]) 

    # Test 3
    q3 = MidSkipQueue(6, range(20))
    # NOTICE: string version is limited by 5 in the output
    assert str(q3) == '[0, 1, 2, 3, 4, ..., 15, 16, 17, 18, 19]'
    assert (
        repr(q3) == 
        'MidSkipQueue(6, [0, 1, 2, 3, 4, 5, ..., 14, 15, 16, 17, 18, 19])'
    )
    assert list(q3[5:9]) == [5, 14, 15, 16]
