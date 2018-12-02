
import timeit 
# timeit.default_timer 
import functools
# functools.wraps

import requests

import logging
logger = logging.getLogger(__name__)


def profile(func):
    """Decorator for adding timing to a function."""

    # Realistically, we'd use logging.debug, along with 
    # delayed interpolation, but we were asked for 'print'
    
    # print_func = logging.warning
    print_func = print
    
    # I'd like to have this option in the Profile func, but 
    # that would be against our specification (again)
    profile_str = "profile[%s]: %s"

    @functools.wraps(func)
    def internal(*args, **kwargs):
        start = timeit.default_timer() 
        res = func(*args, **kwargs)
        end = timeit.default_timer() 

        print_func(
            profile_str % (
                func.__name__,  
                end - start
            )
        )
        return res
    
    return internal


class timer(object):
    """Context manager for timing blocks.
    
    Note
    ----
    I could've done the same with contextlib
    ( https://docs.python.org/3/library/contextlib.html )
    and a decorator 
    """

    def __init__(self, timer_str="timer: %s", print_func=print):
        self.start = None
        self.print_func = print_func
        self.timer_str = timer_str

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, type, value, traceback):
        end = timeit.default_timer() 
        self.print_func(self.timer_str % (end - self.start))


if __name__ == "__main__":
    import time

    @profile
    def f(sec=3):
        time.sleep(sec)
        return sec

    @profile
    def g(sec=3, dlt=0.01):
        print("Hi")
        time.sleep(sec - dlt)
        return sec - dlt

    @profile
    def some_function():
        return sum(range(1000))

    # Just decorator
    f(1)
    g(1)
    result = some_function()

    # Just context manager
    with timer():
        print(sum(range(1000))) 

    # This should set off boh
    with timer("my time is %s, ok?"):
        print(g(0.7))


class SafeRequest(object):
    """Wrapper around Requests that handles timeouts.
    
    Parameters
    ----------
    timeout : float
        Max wait seconds. Default is 3.
    default : SafeRequest.not_set or object
        Default value to return. If not_set, then we raise 
        an exception on 404 instead.
    """

    not_set = object()

    def __init__(self, timeout=3, default=not_set):
        self.timeout = timeout 
        self.default = default 

    def __call__(self, *args, **kwargs):
        """Wraps around requests.request()"""

        # Set timeout forcefully
        kwargs['timeout'] = self.timeout

        # ALTERNATIVE (allows custom timeouts): 
        # kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        
        try:
            res = requests.request(*args, **kwargs)
            res.raise_for_status()
        except requests.ConnectTimeout as e:
            # If we wanted to return default in case of timeout: 
            """
            if self.default is SafeRequest.not_set:
                raise
            res = self.default
            """

            # Since that's not in the spec, we do this:
            raise
        except requests.HTTPError as e:
            # Only fix 404 errors if we have a default value
            if e.response.status_code == 404:
                if self.default is SafeRequest.not_set:
                    raise
                res = self.default
            else:
                raise
        return res

    def get(self, *args, **kwargs):
        """Shorthand for 'get' operations."""
        return self('get', *args, **kwargs)


if __name__ == "__main__":

    # Legit addresses
    p200 = 'http://httpbin.org/status/200'
    yandex = 'http://yandex.ru/'

    # 404 addresses
    p404 = 'http://httpbin.org/status/404'
    y_lol = yandex + 'lol/'

    # Normal Requests code
    d1 = requests.request('get', yandex)
    assert d1.status_code == 200

    d2 = requests.request('get', y_lol)
    assert d2.status_code == 404

    # This should timeout
    try:
        hyper_request = SafeRequest(timeout=0.01, default=None)
        d3 = hyper_request('get', yandex)
    except requests.ConnectTimeout:
        print("Yep, we timed out.")

    # This should find nothing, and return 'whoops'
    safe_request = SafeRequest(timeout=5, default='whoops')
    d4 = safe_request('get', y_lol)
    assert d4 == 'whoops'
