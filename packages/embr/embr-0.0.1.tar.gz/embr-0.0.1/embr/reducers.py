from typing import Callable

from embr.embr import T, S, Embr


class chainable:
    """
    Makes a function chainable with the | operator.
    The decorated function can be used in expressions like:
    func1 | func2 | func3

    @Chainable
    def reducer_1(chat: Embr) -> Spark:
        return Spark("assistant", "[r1] response to: " + chat.last.content)

    @Chainable
    def reducer_2(chat: Embr) -> Spark:
        return Spark("assistant", "[r2] response to: " + chat.last.content)
    """

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__

    def __get__(self, obj, objtype=None):
        """Support descriptor protocol for instance methods"""
        if obj is None:
            return self
        # Create a bound method
        return chainable(self.func.__get__(obj, objtype))

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __lor__(self, other):
        if callable(other):
            return chain_reducers(other, self.func)
        raise TypeError(f"Cannot use | operator with {type(self)} and non-callable {type(other)}")

    def __or__(self, other):
        if callable(other):
            return chain_reducers(self.func, other)
        raise TypeError(f"Cannot use | operator with {type(self)} and non-callable {type(other)}")


def chain_reducers(*reducers: Callable[[T], S]) -> Callable[[T], S]:
    """
    Chain two reducers together so they execute sequentially.
    Returns a new reducer function that applies both in sequence.
    """

    @chainable
    def chained_reducer(embr: T) -> T:
        # Create a new Embr with the same sparks

        for reducer_fn in reducers:
            # Apply the reducer and append the response.
            embr = Embr(embr.sparks.copy())
            response = reducer_fn(embr)
            if isinstance(response, Embr):
                # pass-through
                embr = response
            else:
                # append
                embr << response

        return embr

    return chained_reducer
