# coding=utf-8
"""
Decorator for currying functions.
"""
import inspect


def curry(f):
    """
    The trick here is to replace the decorated function with an object
    whose __call__ magic method simulates beta reduction.

    By necessity, any side effects of `f` do not occur until enough
    arguments have been filled out to perform final evaluation; or,
    equivalently for the lambda wankers, until, given f = λV.E, the
    reduction ((λV.E) E`) →ᵦ λ.E`` has no free variables.

    But you wouldn't use functions that have side effects, you're
    much too smart for that.
    """
    class Curried(object):
        def __init__(self, func, args, kwargs):
            self.func = func
            self.args = args or []
            self.kwargs = kwargs or {}
            spec = inspect.getargspec(func)
            if spec.varargs is not None:
                raise ValueError('cannot curry varargs!')
            if spec.keywords is not None:
                raise ValueError('cannot curry kwargs!')
            self.argnames = spec.args
            self.defaults = spec.defaults

        def __call__(self, *args, **kwargs):
            """
            Argument binding works left to right, or as named. We consider
            it an error to bind any single argument more than once, whether
            this is a named argument specified more than once, or a named
            argument that had previously been filled positionally.

            TODO: maybe it's reasonable to allow positional arguments to be
            bound after keyword arguments? E.g., should the following:

                @curry
                def f(a, b, c): ...

                f(b=1)(2, 3)

            ...be well-defined? It's a fair question.
            """
            if self.kwargs and args:
                raise SyntaxError('non-keyword arg after keyword arg')
            args = self.args + list(args)
            kwargs = dict(self.kwargs.items() + kwargs.items())
            filled = self.argnames[:len(args)]
            unfilled = self.argnames[len(args):]

            # make sure there are no duped kwargs
            for kw in kwargs:
                if kw in filled:
                    raise TypeError('got multiple values for ' + kw)
                if kw not in unfilled:
                    raise TypeError('unexpected argument ' + kw)
                unfilled.remove(kw)

            # TODO: apply defaults

            if unfilled:
                return Curried(self.func, args, kwargs)
            else:
                return self.func(*args, **kwargs)

    return Curried(f, None, None)
