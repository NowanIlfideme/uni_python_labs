

class Node(object):
    def __init__(self, value, next_=None):
        #  a: check input types
        assert(next_ is None or isinstance(next_, Node))
            
        self._value = value
        self._next = next_

    @property
    def next_(self):
        return self._next
    
    @next_.setter
    def next_(self, next_):
        assert(next_ is None or isinstance(next_, Node))
        #  Think: check for existing end of node?
        self._next = next_
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    class _Iterator(object):
        def __init__(self, node=None):
            assert(node is None or isinstance(node, Node))
            self.node = node

        def __next__(self):
            if self.node is None:
                raise StopIteration()
            nd = self.node
            self.node = nd.next_
            return nd.value

    def __iter__(self):
        return Node._Iterator(self)

    def __repr__(self):
        if self._next is None:
            return "%s(%r)" % (self.__class__.__name__, self._value)
        return "%s(%r, %r)" % (
            self.__class__.__name__, self._value, self._next)

    def __str__(self):
        if self._next is None:
            return "[%s]" % (self._value)
        return "[%s] -> %s" % (self._value, self._next)


def _flatten_linked_list(lst):
    """Returns flattened shallow copy of lst and its last node."""
    if lst is None:
        return None, None

    if isinstance(lst.value, Node):
        # shallow copy the sub-list, then find its end
        res, cur = _flatten_linked_list(lst.value)
    else:  # we don't need to flatten any lists
        res = Node(lst.value, None)
        cur = res

    nxt = lst.next_
    while nxt is not None:
        if isinstance(nxt.value, Node):
            head, tail = _flatten_linked_list(nxt.value)
            cur.next_ = head
            cur = tail
        else:  # head==tail
            cur.next_ = Node(nxt.value, None)
            cur = cur.next_
        nxt = nxt.next_
    return res, cur


def flatten_linked_list(lst):
    """Returns a shallow copy of the passed list, while flattening."""

    head, tail = _flatten_linked_list(lst)
    return head


if __name__ == "__main__":
    r1 = Node(1)  # 1 -> None - just one node

    r2 = Node(7, Node(2, Node(9)))  # 7 -> 2 -> 9 -> None

    # 3 -> (19 -> 25 -> None ) -> 12 -> None
    r3 = Node(3, Node(Node(19, Node(25)), Node(12)))
    r3f = flatten_linked_list(r3)  # 3 -> 19 -> 25 -> 12 -> None
    r3fx = [3, 19, 25, 12]
    assert list(r3fx) == list(r3f)

    r4 = Node(Node(Node(19, Node(25)), Node(12)), Node(13))
    r4f = flatten_linked_list(r4)
    r4fx = [19, 25, 12, 13]
    assert list(r4fx) == list(r4f)
