from embr.cache_utils.lru_cache import lru_cache
from dotvar import auto_load  # noqa


def test_lru_mongodb():
    @lru_cache(cache_mode="mongodb")
    def expensive_function(x, y):
        print("Running expensive function")
        import time

        time.sleep(2)
        print("it is done")
        return x + y

    print("starting now")
    for i in range(10):
        expensive_function(1, 3)
