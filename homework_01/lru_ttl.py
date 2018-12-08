"""LRU-TTL cache (Homework #1)."""

from collections import OrderedDict
# from collections.abc import Mapping, Iterator 
from datetime import datetime, timedelta 


class LRU_TTL(object):
    """LRU cache with limited time-to-live on objects.
    
    Paramters
    ---------
    max_size : None or int
        Maximum number of objects in the cache (not memory).
        If None, LRU is inactive.
    ttl : None or float or timedelta
        Default time-to-live (in seconds) of objects in the cache.
        If None, TTL is inactive (objects aren't deleted by time).

    The internal dictionary (_d) is of the format:

        key : (object, end-of-life time (eol))

    
    """

    def __init__(self, max_size=None, ttl=None, elems={}):
        self._max_size = max_size
        self._ttl = ttl

        self._d = OrderedDict()

        for k, v in elems.items():
            self[k] = v

    def __repr__(self):
        s = "%s(max_size=%r, ttl=%r, elems=%r)"
        v = (
            self.__class__.__name__, 
            self._max_size, self._ttl, self._d
        )
        return s % v

    # Properties 

    @property
    def ttl(self):
        """Time-to-live for an object in the cache."""
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        self._ttl = value

    @property
    def max_size(self):
        """Maximum cache size (in objects)."""
        return self._max_size

    @max_size.setter
    def max_size(self, value):
        if (value is None):
            self._max_size = value
        else: 
            self._max_size = int(value)

    # Helpers

    def _find_eol(self, ttl=None):
        """Finds the end-of-life for a current object.
        
        If ttl is None, uses default.
        """
        ttl = ttl or self._ttl  # 
        if ttl is None:
            return datetime.max 
        if not isinstance(ttl, timedelta):
            ttl = timedelta(seconds=ttl)
        return datetime.now() + ttl

    # Basic operations 

    def __len__(self):
        """Returns number of objects currently in cache.
        
        Note that this does not cause invalidation.
        """
        return len(self._d)

    def __setitem__(self, key, value, ttl=None):
        """Sets cache item by key. 
        
        If ttl is None, uses default for self.
        """
        # If we have this key, we need to update
        if key in self._d:
            del self._d[key]
        v = (value, self._find_eol(ttl)) 
        self._d[key] = v
        # remove 'first' (oldest) item, if too long 
        if (self._max_size is not None) and (len(self._d) > self._max_size):
            self._d.popitem(last=False)

    def set(self, key, value, ttl=None):
        """Like subscripting, but can set ttl.
        
        Parameters
        ----------
        key : hashable
            The (hashable) key to use.
        value : object
            Value to store (shallowly).
        ttl : None or float or timedelta
            Time-to-live of this object.
            If None, uses default for this cache.
        """
        self.__setitem__(key, value, ttl=ttl)

    def __getitem__(self, key):
        """Get cache item by key.
        
        Raises KeyError if nonexistant or expired key.
        """ 
        value, eol = self._d[key]
        if eol < datetime.now():
            # Invalidate by removing from self
            del self._d[key]
            raise KeyError("%r (timeout)" % key)
        # Update key
        self._d.move_to_end(key, last=True)
        return value

    def get(self, key, default=None):
        """Like subscripting, but doesn't raise exceptions.
        
        Parameters
        ----------
        key : hashable
            A (hashable) key to find.
        default : None or object
            Default value in case of failure.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        """Delete an object by key."""
        del self._d[key]
    
    def clear(self):
        """Deletes all objects in cache."""
        del self._d  # probably don't need this tbh 
        self._d = OrderedDict()

    def __contains__(self, key, validate=True):
        """Checks if key is in self.
        
        By default, causes validation.
        """
        if validate:
            try:
                self.__getitem__(key)
                return True
            except KeyError:
                return False            
        return key in self._d

    # NOTE: I planned to add iterator methods. 
    # However, because of the TTL part here, I need 
    # to perform invalidation... which means that the 
    # base OrderedDict will possibly be mutated.

#    class _Iterator(Iterator):
#        """Iterator for the LRU-TTL cache."""
#
#        def __init__(self, cache):
#            self.cache = cache
#            self.key_it = iter(cache._d)
#
#        def __next__(self):
#            while True:
#                try:
#                    key = next(self.key_it)
#                    val = self.cache[key]
#                except KeyError:
#                    
#
#    def __iter__(self):
#        return self._Iterator(self)
