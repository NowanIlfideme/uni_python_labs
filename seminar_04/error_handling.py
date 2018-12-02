
import time
import traceback
import functools
import logging
from collections.abc import Iterable
logger = logging.getLogger(__name__)


class handle_error_context(object):
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

    def __init__(
        self, re_raise=True, log_traceback=True, 
        exc_type=Exception
    ):
        self.re_raise = bool(re_raise)
        self.log_traceback = bool(log_traceback)

        # Turn exc_type into a tuple, always;
        # even if it's a single exception.
        if not isinstance(exc_type, Iterable):
            exc_type = (exc_type, )
        self.exc_type = tuple(exc_type)

    def __enter__(self):
        # Do nothing on entrance. ;)
        pass

    def __exit__(self, type, value, trace):
        # Check if we want to handle this exception
        if not any(issubclass(type, xt) for xt in self.exc_type):
            return  # will automatically re-raise

        if self.log_traceback:
            logging.exception("Context caught exception:")
            # This will automatically add the traceback to log
            # and no need for traceback lib stuff
        if self.re_raise:
            return  # will automatically re-raise 
        return True


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

    global_tries = tries
    global_delay = delay
    
    # Returns this decorator...
    def decorator(func):
        # ... that wraps the function...
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # ... with the context manager...

            tries = global_tries
            delay = global_delay 

            tb = None
            exc = None
            success = False
            while not success and (tries is None or tries > 0):
                try:
                    res = func(*args, **kwargs)
                    success = True
                except exc_type as e:
                    if tries is not None:
                        tries -= 1
                    tb = traceback.format_exc()
                    exc = e

                    # waiting
                    time.sleep(delay)
                    delay *= backoff
            if success:
                if tb is not None:
                    logging.error("Caught exception:\n%s" % tb)
                return res
            
            raise exc
        return wrapped
    return decorator


if __name__ == "__main__":
    with handle_error_context(
        re_raise=False, log_traceback=True, exc_type=ValueError
    ):
        raise ValueError()
    # Prints traceback

    @handle_error(re_raise=False)
    def some_function():
        return 1 / 0  # ZeroDivisionError
    
    some_function()
    # Didn't test :(

    # Time test, kinda
    import random

    @handle_error(re_raise=True, tries=3, delay=0.5, backoff=2)
    def some_function():
        if random.random() < 0.75:
            x = 1 / 0 # ZeroDivisionError
    some_function()
