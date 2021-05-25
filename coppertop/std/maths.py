# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)

_EPS = 7.105427357601E-15      # i.e. double precision


import builtins

from .._core import Missing
from .._pipe import pipeable, binary

try:
    import numpy
except:
    numpy = Missing


@pipeable(flavour=binary)
def closeTo(a, b, tolerance=_EPS):
    if abs(a) < tolerance:
        return abs(b) < tolerance
    else:
        return abs(a - b) / abs(a) < tolerance

@pipeable
def within(x, a, b):
    # answers true if x is in the closed interval [a, b]
    return (a <= x) and (x <= b)

@pipeable
def mean(ndOrPy):
    # should do full numpy?
    return numpy.mean(ndOrPy)

@pipeable
def std(ndOrPy, dof=0):
    # should do full numpy? std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)
    return numpy.std(ndOrPy, dof)

@pipeable
def sqrt(x):
    return numpy.sqrt(x)

@pipeable
def max(iter):
    return builtins.max(iter)

@pipeable
def min(iter):
    return builtins.min(iter)
