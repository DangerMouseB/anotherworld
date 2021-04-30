# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


import itertools
import numpy as np

from .._core import NotYetImplemented
from .._pipe import pipeable, binary, ternary, binary2, unary1
from .struct import struct, _nd, nd

# iter iteration (rather than range iteration)


@pipeable(flavour=ternary)
def both(a, f, b):
    if isinstance(a, _nd):
        with np.nditer([a.nd, b.nd, None]) as it:
            for x, y, z in it:
                z[...] = f(x,y)
            return nd(it.operands[2])
    else:
        return [f(x, y) for (x, y) in zip(a, b)]


@pipeable(flavour=binary2)
def each(xs, f):
    """each(xs, f)  e.g. xs >> each >> f
    Answers [f(x) for x in xs]"""
    if isinstance(xs, struct):
        inputsAndOutput = [x.nd for x in xs._values()] + [None]
        with np.nditer(inputsAndOutput) as it:
            for vars in it:
                vars[-1][...] = f(*vars[:-1])
            return nd(it.operands[len(inputsAndOutput)-1])
    else:
        return [f(x) for x in xs]


@pipeable(flavour=binary)
def ieach(xs, f2):
    """each(xs, f)  e.g. xs >> each >> f
    Answers [f(i, x) for x in enumerate(xs)]"""
    return [f2(i, x) for (i, x) in enumerate(xs)]


def _where(s, bools):
    assert isinstance(s, struct)
    answer = struct(s)
    for f, v in s._fvPairs():
        answer[f] = nd(v.nd[bools.nd])
    return answer
where = binary2('where', binary2, _where)


@pipeable(flavour=binary2)
def filter(xs, f):
    """each(xs, f)  e.g. xs >> filter >> f
    Answers [x for x in xs if f(x)]"""
    return [x for x in xs if f(x)]


@pipeable(flavour=binary)
def inject(xs, seed, f2):
    prior = seed
    for x in xs:
        prior = f2(prior, x)
    return prior


@pipeable(flavour=binary2)
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


dict_keys = type({}.keys())
@pipeable(flavour=unary1)
def materialise(x):
    if isinstance(x, dict_keys):
        return list(x)
    else:
        raise NotYetImplemented()


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
