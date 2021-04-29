# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable, binary, ternary


# iter iteration (rather than range iteration)

@pipeable(flavour=binary)
def each(xs, f):
    """each(xs, f)  e.g. xs >> each >> f
    Answers [f(x) for x in xs]"""
    return [f(x) for x in xs]

@pipeable(flavour=binary)
def filter(xs, f):
    """each(xs, f)  e.g. xs >> filter >> f
    Answers [x for x in xs if f(x)]"""
    return [x for x in xs if f(x)]

@pipeable(flavour=ternary)
def eachBoth(xs, fn2, ys):
    return [fn2(x, y) for (x, y) in zip(xs, ys)]

@pipeable(flavour=binary)
def inject(xs, seed, f2):
    prior = seed
    for x in xs:
        prior = f2(prior, x)
    return prior

@pipeable(flavour=binary)
def chunkUsing(iter, fn2):
    answer = []
    i0 = 0
    for i1, (a, b) in enumerate(_pairwise(iter)):
        if not fn2(a, b):
            answer += [iter[i0:i1+1]]
            i0 = i1 + 1
    answer += [iter[i0:]]
    return answer

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


# @pipeable
# def Chain(seed, xs, f):
#     """chain(seed, xs, f)    e.g. xs >> Chain(seed) >> f
#     Answers resultn where resulti=f(prior, xi) for each x in xs
#     prior = resulti-1 or seed initially"""
#     prior = seed
#     for x in xs:
#         prior = f(prior, x)
#     return prior
#
# @pipeable
# def EachArgs(listOfArgs, f):
#     """eachArgs(f, listOfArgs)
#     Answers [f(*args) for args in listOfArgs]"""
#     return [f(*args) for args in listOfArgs]
