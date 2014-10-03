# coding=utf-8
"""
Decorator for currying functions.
"""
import inspect


def curry(f):
    """
    The trick here is to replace the decorated function `f` with a
    function that simulates beta reduction of `f`.

    By necessity, any side effects of `f` do not occur until enough
    arguments have been filled out to perform final evaluation; or,
    equivalently for the lambda wankers, until, given f = λV.E, the
    reduction ((λV.E) E`) →ᵦ λ.E`` has no free variables.

    But you wouldn't use functions that have side effects, you're
    much too smart for that.
    """

    spec = inspect.getargspec(f)
    if spec.varargs is not None:
        raise ValueError('cannot curry varargs')
    if spec.keywords is not None:
        raise ValueError('cannot curry kwargs')

    # Value representing an unbound variable
    undefined = object()

    # Map argspec defaults to their parameter names
    defaults = {
        spec.args[-i]: spec.defaults[-i]
        for i in range(1, len(spec.defaults)+1)
    } if spec.defaults is not None else {}

    def beta(bindings, *args, **kwargs):
        """
        This function implements the 'beta reduction'-like step by binding
        positional arguments left-to-right, then binding keyword arguments,
        finally checking if the underlying function is fully bound (after
        accounting for default arguments).
        """
        args = list(args)
        bindings = list(bindings)

        for i, (name, value) in enumerate(bindings):
            if args and value is undefined:
                bindings[i] = (name, args.pop(0))
            if name in kwargs:
                bindings[i] = (name, kwargs.pop(name))

        if args:
            raise TypeError('too many positional arguments', args)
        if kwargs:
            raise TypeError('unexpected keyword arguments', kwargs)

        callargs = map(lambda (name, value): value is not undefined and value
                       or defaults.get(name, undefined), bindings)

        if undefined in callargs:
            return lambda *args, **kwargs: beta(bindings, *args, **kwargs)
        else:
            return f(*callargs)

    # Start with a nullary beta reduction
    return beta(((name, undefined) for name in spec.args))
