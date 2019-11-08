import inspect


class CachedInstanceMethodMixin(object):
    def cache_clear(self):
        """
        Calls `clear_cache` method on all bound methods in this instance
        (where valid).
        Intended to clear calls cached with the `memoize` decorator.
        Note that this will also clear functions decorated with `lru_cache` and
        `lfu_cache` in this class (or any other function with `clear_cache`
        attribute).
        """
        for _, method in inspect.getmembers(self, inspect.ismethod):
            try:
                method.cache_clear()
            except (AttributeError, TypeError):
                pass
