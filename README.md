curried
=======

A small and probably inadvisable library for creating transparently curried
functions in Python, because those are totally what Python needs.

Simple example
--------------

Currying functions with `curried` is so easy, it's stupid!

    from curried import curry
    
    @curry
    def foo(a, b, c, d=1):
        return sum((a*1000, b*100, c*10, d))

    assert foo(b=3)(4)(2) == 4321

As you can see from the example, `curried` supports default arguments and
keyword arguments, including binding keyword arguments before positional
arguments.

Each application of a curried function represents (almost) the process of
beta reduction by using partial application. Each reduction can specify any
positional or keyword arguments that can be bound in the function; positional
arguments are bound in order, and attempting to bind more positional arguments
than there are free variables in the function will result in a `TypeError`.
Keyword arguments have no such restriction, and may even overwrite previously
bound arguments.

By necessity, any side effects of a curried function `f` do not occur until
enough arguments have been filled out to perform final evaluation; or,
equivalently for the lambda wankers (you know who you are), until, given
*f = λV.E*, the reduction *((λV.E) E') →ᵦ λ.E''* has no free variables.

There is also the limitation that functions whose signatures contain `*args`
or `**kwargs` cannot be curried.


A much more frightening example
-------------------------------

This library aims to introduce some of the glories of functional programming
to the desolate wasteland that is Python, and what better way to do that than
by horribly mangling its standard libraries? With `curried`, you can sprinkle
some of Haskell Curry's magic fairy dust over any other module you choose:

    from curried import re

    numbers = re.findall('\d+')

    text1 = 'I will trade you 14 apricots for your 3 aircraft carriers.'
    text2 = 'The 12 handbags contained 802 mice, 4 badgers, and 1 squirrel.'

    assert numbers(text1) == ['14', '3']
    assert numbers(text2) == ['12', '802', '4', '1']

Doubtless this mad enterprise will be expanded in the future to shovel even
more kinds of function-munging into Python's alarmingly flexible code hole.
God help us all.
