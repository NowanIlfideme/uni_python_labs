
import time
# import traceback
import functools
import logging
import itertools
import contextlib
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def handle_error_context(
    re_raise=True, log_traceback=True, 
    exc_type=Exception, 
):
    """Error-handling context.

    Parameters
    ----------
    re_raise : bool
        Whether to re-raise `exc_type` exceptions.
        Default is True.
    log_traceback : bool
        Whether to show traceback for `exc_type` expections.
        Default is True.
    exc_type : type or tuple
        Exception type (or tuple of exception types) to catch;
        all others will be ignored. Default is Exception.
    """
    try:
        yield
    except exc_type as e:
        if log_traceback:
            logging.exception("Context caught:")
        if re_raise:
            raise


def handle_error(
    re_raise=True, log_traceback=True, 
    exc_type=Exception, tries=1, delay=0, backoff=1, 
):
    """
    Parameters
    ----------
    re_raise : bool
        Whether to re-raise `exc_type` exceptions.
        Default is True.
    log_traceback : bool
        Whether to show traceback for `exc_type` expections.
        Default is True.
    exc_type : type or tuple
        Exception type (or tuple of exception types) to catch;
        all others will be ignored. Default is Exception.
    tries : int or None
        Number of times to try calling before giving up.
        None represents infinite tries. If int, must be positive.
        Default is 1.
    delay : float
        Delay between retries, in seconds. Default is 0.
    backoff : float
        Number to multiply delay by after each try. Default is 1.
    """

    # Returns this decorator...
    def decorator(func):
        # ... that wraps the function...

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # ... with the context manager...

            # initialize delay and "counter" for tries
            curr_delay = delay
            if tries is None:
                rng = itertools.repeat(9)
            else:
                rng = range(tries, 0, -1)

            for n_left in rng:
                try:
                    with handle_error_context(
                        # force re-raising if we fail
                        # except the last one (where we use defined)
                        re_raise=(n_left > 1) or re_raise, 
                        # log every time, if set
                        log_traceback=log_traceback, 
                        # same exceptions
                        exc_type=exc_type, 
                    ):
                        res = func(*args, **kwargs)
                        return res
                except exc_type as e:
                    if n_left > 1:
                        time.sleep(curr_delay)
                        curr_delay *= backoff
                    else:
                        # we've reached end of line
                        raise 
        return wrapped
    return decorator


if __name__ == "__main__":
    import random

    random.seed(42)

    def zprint(*args, **kwargs):
        print("-----------")
        print(*args, **kwargs)

    # Example 1
    zprint("EXAMPLE 1")
    # Prints stacktrace, no reraise
    with handle_error_context(
        re_raise=False, log_traceback=True, exc_type=ValueError
    ):
        raise ValueError()
    
    # Example 2
    zprint("EXAMPLE 2")
    # Prints stacktrace, but no exception  
       
    @handle_error(re_raise=False)
    def f2():
        return 1 / 0  # ZeroDivisionError
    f2()
    
    # Example 3
    zprint("EXAMPLE 3")
    # Only raises exception, because wrong type

    @handle_error(re_raise=False, exc_type=KeyError)
    def f3():
        return 1 / 0  # ZeroDivisionError
    try:
        f3()
    except ZeroDivisionError:
        print("Yay, we caught it")

    # Example 4
    zprint("EXAMPLE 4")
    # Retries multiple times, before giving up
    # Raises 4 times

    @handle_error(re_raise=True, tries=4, delay=1, backoff=2)
    def f4(val=1):
        if random.random() < val:
            print(1 / 0)  # ZeroDivisionError
    try:
        f4()
    except ZeroDivisionError:
        print("Yep, they were ALL failures...")
