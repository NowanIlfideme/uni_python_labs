
import abc


class BoundedMeta(type):
    """Metaclass that limits number of instantiated objects."""

    #@classmethod
    #def __prepare__(metacls, name, bases, **kwargs):
    #    # kargs = {"myArg1": 1, "myArg2": 2}
    #    return super().__prepare__(name, bases, **kwargs)
    
    _instances = {}

    def __new__(metacls, name, bases, dct, max_instance_count=1):
        # mic = dct.get('max_instance_count', 0)  
        cls = super().__new__(metacls, name, bases, dct)
        cls.max_instance_count = max_instance_count
        
        return cls
    
    def __call__(cls, *args, **kwargs):
        n = cls._instances.get(cls, 0)
        max_n = cls.max_instance_count
        if (max_n is not None) and (n >= max_n):
            raise TypeError(
                "Too many instances! Max is %s." % max_n
            )
        
        # NOTE: Increasing ahead of time to try to prevent
        # race conditions... realistically, GIL helps most 
        # of the time, and there's still a possibility of 
        # making too many objects anyways... whatever. :P
        cls._instances[cls] = n + 1
        try:
            res = super().__call__(*args, **kwargs)
        except Exception:
            cls._instances[cls] -= 1
            raise
        
        return res


class BoundedBase(metaclass=abc.ABCMeta):
    """"""

    _instances = {}

    @abc.abstractclassmethod
    def get_max_instance_count(cls):
        """Gets maximum number of instances for this class."""
        return 1

    def __new__(cls, *args, **kwargs):
        n = cls._instances.get(cls, 0)
        max_n = cls.get_max_instance_count()
        
        if (max_n is not None) and (n >= max_n):
            raise TypeError(
                "Too many instances! Max is %s." 
                % max_n
            )

        cls._instances[cls] = n + 1
        try:
            res = super().__new__(cls, *args, **kwargs)
        except Exception:
            cls._instances[cls] -= 1
            raise
        
        return res


if __name__ == "__main__":

    # Example 5
    for n in [1, 3, 0]:
        class C(metaclass=BoundedMeta, max_instance_count=n):
            pass

        cs = [C() for _ in range(n)]        
        try:
            c = C()
        except TypeError as e:
            print("Works fine. We got:", e)
        else:
            print("Something went wrong. :(")
        print("Objects made:", len(cs))

    # Example 6
    for n in [1, 3, 0]:
        class D(BoundedBase):
            @classmethod
            def get_max_instance_count(cls): 
                return n
        
        ds = [D() for _ in range(n)]
        try:
            d2 = D()
        except TypeError as e:
            print("Works fine. We got:", e)
        else:
            print("Something went wrong. :(")
        print("Objects made:", len(ds))

    # Test out max==None
    class C(metaclass=BoundedMeta, max_instance_count=None):
        pass
    
    class D(BoundedBase):
        @classmethod
        def get_max_instance_count(cls): 
            return None

    try:
        cs = [C() for _ in range(10)]
        ds = [D() for _ in range(10)]
        print("Everything worked for (max==None)! :)")
    except Exception as e:
        print("Incorrect. Exception:\n", e)
