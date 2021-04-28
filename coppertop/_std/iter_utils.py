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

# @pipeable
# def EachIf(xs, f, ifF):
#     """each(xs, f)  e.g. xs >> EachIf >> f >> ifF
#     Answers [f(x) for x in xs]"""
#     return [f(x) for x in xs if ifF(x)]
#
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
