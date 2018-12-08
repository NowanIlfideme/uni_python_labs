
import unittest
from lru_ttl import LRU_TTL
from time import sleep
from datetime import timedelta 


class Test_LRUTTL(unittest.TestCase):

    def test_lru(self):
        """Tests LRU (no-time) capabilities."""

        a = LRU_TTL(max_size=4)

        for i in range(6):
            a[i] = i * 10
        
        self.assertDictEqual(
            {2: 20, 3: 30, 4: 40, 5: 50},
            a.to_dict()
        )
        a[4]

        # Order must chang
        self.assertDictEqual(
            {2: 20, 3: 30, 5: 50, 4: 40},
            a.to_dict()
        )
        a[9] = 90
        self.assertDictEqual(
            {3: 30, 5: 50, 4: 40, 9: 90},
            a.to_dict()
        )

        # Alternatives for "get"
        with self.assertRaises(KeyError):
            a[1337]

        self.assertEqual(a.get(8008), None)

    def test_nomax_operations(self):
        """Tests limitless cache, and operations."""

        a = LRU_TTL()

        for i in range(100):
            a[i] = i * 10
        
        for i in range(100):
            self.assertTrue(i in a)
            a[i]

        # Check deletion 
        b = LRU_TTL()
        b[8] = 8
        b[9] = 9
        del b[8]
        with self.assertRaises(KeyError):
            b[8]
        b.clear()
        with self.assertRaises(KeyError):
            b[9]

        # Check __contains__
        c = LRU_TTL()
        dct = {1: 2, 'a': 4, 3: 'k'}
        for k, v in dct.items():
            c[k] = v
        self.assertTrue(all(k in c for k in dct))

    def test_ttl(self):
        """Tests timing (for limitless cache)."""

        t = 0.05
        d = 0.01
        a = LRU_TTL(ttl=t)

        # Normal timeout
        with self.assertRaises(KeyError):
            a[1] = 10
            sleep(t + d)
            a[1]
        
        # Normal work (then timeout)
        a[2] = 10
        a[3] = 10
        sleep(t - d)
        a[2]
        with self.assertRaises(KeyError):
            sleep(d * 2)
            a[3]

        # Setting with a shorter timeout
        with self.assertRaises(KeyError):
            a.set(4, 10, ttl=t - d)
            sleep(t)
            a[4]

        # Setting with (basically) infinite timeout
        a.set(5, 10, ttl=timedelta(days=1))
        a[5]

        # Can't do this because of, well... overflow.
        with self.assertRaises(OverflowError):
            a.set(6, 10, ttl=timedelta.max)
            a[6]


if __name__ == "__main__":
    unittest.main()
