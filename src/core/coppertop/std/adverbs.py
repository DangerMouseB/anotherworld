# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import itertools, builtins
import numpy as np

from coppertop.pipe import pipeable, unary1, binary, binary2, ternary
from .struct import struct, _nd, nd
from .testing import assertEquals
from ._core import _


@pipeable(flavour=ternary)
def both(a, f, b):
    if isinstance(a, _nd):
        with np.nditer([a.nd, b.nd, None]) as it:
            for x, y, z in it:
                z[...] = f(x,y)
            return nd(it.operands[2])
    else:
        return [f(x, y) for (x, y) in builtins.zip(a, b)]


@pipeable(flavour=binary2)
def each(xs, f):
    """each(xs, f)  e.g. xs >> each >> f
    Answers [f(x) for x in xs]"""
    # if isinstance(xs, struct):
    #     inputsAndOutput = [x.nd for x in xs._values()] + [None]
    #     with np.nditer(inputsAndOutput) as it:
    #         for vars in it:
    #             vars[-1][...] = f(*vars[:-1])
    #         return nd(it.operands[len(inputsAndOutput)-1])
    # elif isinstance(xs, struct):
    # else:
    return [f(x) for x in xs]


@pipeable(flavour=binary2)
def ieach(xs, f2):
    """each(xs, f)  e.g. xs >> each >> f
    Answers [f(i, x) for x in enumerate(xs)]"""
    return [f2(i, x) for (i, x) in enumerate(xs)]


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

def _test_inject():
    [1,2,3] >> inject(_,0,_) >> (lambda a,b: a + b) >> assertEquals >> 6


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
    return builtins.zip(a, b)


@pipeable(flavour=unary1)
def zip(x):
    return builtins.zip(*x)


@pipeable(flavour=binary2)
def pushAllTo(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR


@pipeable(flavour=binary2)
def eachAsArgs(listOfArgs, f):
    """eachAsArgs(f, listOfArgs)
    Answers [f(*args) for args in listOfArgs]"""
    return [f(*args) for args in listOfArgs]