import time
# Simple retry decorator if backoff_utils is missing
def with_retry(max_tries=3, exceptions=(Exception,), delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    tries += 1
                    if tries >= max_tries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator