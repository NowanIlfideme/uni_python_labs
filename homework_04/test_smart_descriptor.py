
import unittest
import os 
from smart_descriptor import smart_property 


class A(object):
    """Example class."""

    @smart_property
    def p(self):
        """
        Path-specific test.

        :type: str
        :default: ./docs

        :check_exists 
        :abspath 
        """
        pass

    @smart_property
    def p2(self):
        """
        Path-specific test, but doesn't exist.

        :type: str
        :default: ./nonexistant-path


        :check_exists 
        :abspath 
        """
        pass

    @smart_property
    def p3(self):
        """
        Path-specific test, create pls.

        :type: str
        :default: ./create_pls.txt

        :check_exists 
        :abspath 
        :create_if_not_exists  
        """
        pass

    @smart_property
    def q(self):
        """
        Another property.

        :type: float
        :default: 100

        :mandatory
        """
        pass

    @smart_property
    def r(self):
        """
        Readonly property.

        :type: int
        :default: 5

        :readonly 
        :mandatory
        """
        pass


class B(object):
    """Another example class."""


class Test_smart_property(unittest.TestCase):
    """Tests the smart_property.
    
    Honestly, these are pretty basic test cases.
    We'd """

    def setUp(self):
        dcs = './docs'
        if not os.path.exists(dcs):
            os.mkdir(dcs)  # for a.p

        self.a = A()
        self.b = B()

    def tearDown(self):
        os.rmdir('./docs')  # for a.p

        pt = self.a.p3
        # NOTE: no race condition during test, so whatever
        if os.path.exists(pt):
            os.remove(pt)
        
    def test_p(self):
        """Tests A.p, p1, p2 properties."""

        a = self.a

        with self.assertRaises(AttributeError):
            a._p  # because we didn't ever access a.p
        self.assertEqual(a.p, os.path.abspath('./docs'))
        a._p

        a.p = './pics'

        with self.assertRaises(ValueError):
            a.p2  # because the path doesn't exist!

        # This will automatically make the path
        self.assertTrue(os.path.exists(a.p3))
        # NOTE: it's later killed by self.tearDown()

    def test_r(self):
        """Tests A.r property (readonly)"""

        a = self.a        

        a.r

        with self.assertRaises(AttributeError):
            a.r = 4  # because readonly

        # Still allowed to cheat
        a._r = 4
        self.assertEqual(a.r, 4)

    def test_q(self):
        """Tests A.q property (float, mandatory)"""

        a = self.a  

        # Accept any of the following formats
        a.q = 101
        a.q = '99.9'
        self.assertAlmostEqual(a.q, 99.9, places=2)
        
        a.q = '0xBEEF'

        with self.assertRaises(ValueError):
            a.q = 'BEEF'  # not a valid hex literal


if __name__ == "__main__":
    unittest.main()
