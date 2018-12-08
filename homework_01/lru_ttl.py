"""LRU-TTL cache (Homework #1)."""


class LRU_TTL(object):
    """LRU cache with limited time-to-live on objects.
    
    Paramters
    ---------
    max_size : None or int
        Maximum number of objects in the cache (not memory).
        If None, LRU is inactive.
    ttl : None or float
        Default time-to-live (in seconds) of objects in the cache.
        If None, TTL is inactive (objects aren't deleted by time).
    """

    def __init__(self, max_size=None, ttl=None):
        self._max_size = max_size
        self._ttl = ttl

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
        self._max_size = value
    
    def __len__(self):
        """Returns number of objects currently in cache."""
        # TODO

    def __setitem__(self, key, value, ttl=None):
        """Sets cache item by key. 
        
        If ttl is None, uses default."""
        # TODO

    def __getitem__(self, key):
        """Get cache item by key."""
        # TODO

    def __delitem__(self, key):
        """Delete an object by key."""
        # TODO
    
    def clear(self):
        """Deletes all objects in cache."""
        # TODO

    def __contains__(self, key):
        """Checks if key is in object."""
        # TODO
