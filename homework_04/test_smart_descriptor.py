
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


a = A()
a.p
a.q
a.r

# NOTE: these are only generated upon access at least one
# I couldn't figure out how to get the parent from __new__ or __init__ :/
a._p
a._q
a._r

#
a.q = 101
a.q = '99.9'

try:
    a.r = 4
except AttributeError:
    print("All good!")


class B(object):
    """Another example class."""


try:
    a.p2
except ValueError as e:
    print("All good: %s" % e)

print(
    "Path exists (%s): %s",
    os.path.exists(a.p3),
    a.p3
)
