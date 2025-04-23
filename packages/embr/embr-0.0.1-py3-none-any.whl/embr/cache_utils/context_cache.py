import re

from scratch.cache_utils.lru_cache import lru_cache


def _replace_substring(test_str, s1, s2):
    # Replacing all occurrences of substring s1 with s2
    assert s1 != ".", "s1 cannot be '.' because tha matches every character."
    test_str = re.sub(s1, s2, test_str)
    return test_str


class context_cache(lru_cache):
    """A decorator that implements a context caching mechanism.

    Usage:
        def
    """

    context = []

    def __call__(self, *args, _no_cache=False, **kwargs):
        current_ctx = self.context[-1]
        response = self.func(*args, **kwargs, _context=current_ctx)

        key = self.cache.hash_fn({"_args": args, **kwargs})
        # short_key = self.cache.short_hash_fn(hash=key)

        # note: move the not using cache at the beginning. Otherwise the key
        #   check blocks execution.
        if self.use_cache and (not _no_cache) and key in self.cache:
            # Cache hit - return the cached result
            self.last_hit = True
            result = self.cache[key]
        elif self.is_method:
            # This is a method call (detected by __get__)
            # We need to pass the bound instance as the first argument
            self.last_hit = False
            result = self.func(self.bound_instance, *args, **kwargs)
        else:
            # This is a regular function call
            self.last_hit = False
            result = self.func(*args, **kwargs)

        # note: not ideal.
        if self.use_cache and self.cache.get(key, None) != result:
            # use the doc_id as the context_id.
            self.cache[key] = result

        return result

    def __lor__(self, value):
        pass

    def clear_cache(self):
        self.cache.clear()


if __name__ == "__main__":

    @context_cache
    def expensive_function(x, y):
        print("Running expensive function")
        import time

        time.sleep(2)
        print("it is done")
        return x + y

    print("starting now")
    for i in range(10):
        expensive_function(1, 3)
