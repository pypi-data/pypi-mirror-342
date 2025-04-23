import re

from .mongodb_cache import MongoDBCache
from .pickle_cache import PickleCache


def _replace_substring(test_str, s1, s2):
    # Replacing all occurrences of substring s1 with s2
    assert s1 != ".", "s1 cannot be '.' because tha matches every character."
    test_str = re.sub(s1, s2, test_str)
    return test_str


class lru_cache(object):
    """A decorator that implements a Least Recently Used (LRU) caching mechanism.
    Can be used to cache function results in either MongoDB or pickle file storage.

    This class implements the descriptor protocol (via __get__) to support both function and method decoration:

    1. When used to decorate a function:
       - The decorator is applied directly
       - The function is called normally via __call__

    2. When used to decorate a method:
       - The __get__ method is automatically called by Python when the method is accessed
       - __get__ captures the instance (self) of the class the method belongs to
       - When the method is called, __call__ passes the captured instance as the first argument

    This dual behavior allows the same decorator to work seamlessly with both standalone functions
    and class methods without requiring different implementations.

    Examples:
        # Function decoration - __get__ is never called
        @lru_cache
        def expensive_calculation(x, y):
            return x + y

        result = expensive_calculation(1, 2)  # Calls __call__ directly

        # Method decoration - __get__ is called when accessing the method
        class Calculator:
            @lru_cache
            def expensive_calculation(self, x, y):
                return x + y

        calc = Calculator()
        # When accessing calc.expensive_calculation, __get__ is called
        # When calling calc.expensive_calculation(1, 2), __call__ is called
        result = calc.expensive_calculation(1, 2)
    """

    is_method = False

    def __get__(self, instance, owner):
        """Descriptor protocol method that enables the decorator to work with instance methods.
        When decorating a method, this captures the instance to properly bind 'self'.

        This method is automatically called by Python when accessing a decorated method on a class instance.
        It stores the instance object so that when the method is called, we can pass the instance as the first
        argument (self) to the original method.

        Args:
            instance: The instance that the decorated method belongs to
            owner: The class that owns the decorated method

        Returns:
            The decorator instance itself, which will handle the actual method call via __call__
        """

        self.bound_instance = instance
        self.is_method = True

        return self

    def __new__(cls, func=None, **deps):
        """Factory method to support both direct decoration (@lru_cache)
        and parameterized decoration (@lru_cache(cache_mode='mongodb')).

        Args:
            func: The function to be decorated
            **deps: Additional decorator parameters
        """
        if func is None:
            return lambda fn: lru_cache(fn, **deps)

        cache_instance = super().__new__(lru_cache)
        return cache_instance

    def __init__(self, func=None, cache_mode="pickle"):
        """Initialize the cache decorator with the given function and cache storage mode.

        Args:
            func: The function to be decorated
            cache_mode: Storage backend for the cache, either 'pickle' or 'mongodb'
        """
        assert func is not None, "None case should be handled by __new__"

        self.func = func

        if cache_mode == "mongodb":
            # print("\n ==> splitting", func.__module__, flush=True)
            # what if it does not contain
            try:
                root_module, modules = func.__module__.split(".", 1)
            except ValueError:
                root_module = "__scripts__"
                modules = func.__module__

            prefix = _replace_substring(modules, "\.", "-")
            print("instantiating mongo_cache")
            self.cache = MongoDBCache(f"{prefix}-{func.__name__}", db_name="cache-" + root_module)

            self.cache.load()
            self.use_cache = True

        elif cache_mode == "pickle":
            self.cache = PickleCache(func.__name__, cache_dir=".cache/" + func.__module__)

            self.cache.load()
            self.use_cache = True
        else:
            self.use_cache = False

    def set_cache(self, state=True):
        self.use_cache = state

    def __call__(self, *args, _no_cache=False, **kwargs):
        """
        This is the method that is called when the decorated function is called.
        Pass _no_cache=True to bypass the cache.

        This method handles both function and method calls:
        - For functions: Simply calls the original function with the provided arguments
        - For methods: Uses the instance captured by __get__ to call the original method
          with the proper 'self' reference

        Args:
            *args: Positional arguments to pass to the decorated function
            _no_cache: If True, bypasses the cache and always executes the function
            **kwargs: Keyword arguments to pass to the decorated function

        Returns:
            The result of the function call, either from cache or from execution
        """

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

    def clear_cache(self):
        self.cache.clear()


if __name__ == "__main__":

    @lru_cache
    def expensive_function(x, y):
        print("Running expensive function")
        import time

        time.sleep(2)
        print("it is done")
        return x + y

    print("starting now")
    for i in range(10):
        expensive_function(1, 3)
