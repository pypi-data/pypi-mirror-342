from datetime import datetime, timedelta
import functools


def timed_cache(**timedelta_kwargs):

    def _wrapper(f):
        maxsize = timedelta_kwargs.pop('maxsize', 128)
        typed = timedelta_kwargs.pop('typed', False)
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() - update_delta
        # Apply @lru_cache to f
        f = functools.lru_cache(maxsize=maxsize, typed=typed)(f)
        print("befor", f.cache_info())

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                print("befor", f.cache_info())
                f.cache_clear()
                print("After", f.cache_info())
                next_update = now + update_delta
            return f(*args, **kwargs)
        return _wrapped
    return _wrapper
