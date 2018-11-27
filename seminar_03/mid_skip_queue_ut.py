
import unittest
from mid_skip_queue import MidSkipQueue, MidSkipPriorityQueue


class Test_queues(unittest.TestCase):
    """Simple unit tests (mostly just the given examples)."""

    def test_normal_queue_mechanics(self):
        q = MidSkipQueue(1) 
        q.append(-1)  # q: [-1]
        q += (-2, -3)  # q: [-1, -3] - the first and the last remain
        self.assertEqual(list(q), [-1, -3]) 
        q.append(4)  # q: [-1, 4] - the last item has been replaced
        self.assertEqual(list(q), [-1, 4]) 
        self.assertEqual(q[-1], 4) 

        q2 = MidSkipQueue(2, [1, 2, 3, 4, 5]) 
        self.assertEqual(q2.index(4), 2) 
        self.assertEqual(q2.index(3), -1)  # not in q2, funnily enough
        self.assertEqual(list(MidSkipQueue(1, q2)), [1, 5]) 

        q2b = q2 + [-1, 7] 
        self.assertTrue(5 not in q2b) 
        self.assertEqual(list(q2b), [1, 2, -1, 7]) 
        self.assertEqual(q2b, q2 + q + [7])

    def test_normal_queue_repr(self):
        q3 = MidSkipQueue(6, range(20))
        # NOTICE: string version is limited by 5 in the output
        self.assertEqual(str(q3), '[0, 1, 2, 3, 4, ..., 15, 16, 17, 18, 19]')
        self.assertEqual(
            repr(q3), 
            'MidSkipQueue(6, [0, 1, 2, 3, 4, 5, ..., 14, 15, 16, 17, 18, 19])'
        )
        self.assertEqual(list(q3[5:9]), [5, 14, 15, 16])

    def test_priority_queue(self):
        """Tests mspq and repr"""
        p = MidSkipPriorityQueue(1)
        p.append(-1)
        p += (-2, -3)
        self.assertEqual(list(p), [-3, -1])
        p.append(4)
        self.assertEqual(list(p), [-3, 4])
        p.append(-5)
        self.assertEqual(list(p), [-5, 4])
        self.assertEqual(str(p), '[-5, ..., 4]')
        self.assertEqual(
            repr(p), 
            'MidSkipPriorityQueue(1, [-5, ..., 4])'
        )


if __name__ == '__main__':
    unittest.main()
