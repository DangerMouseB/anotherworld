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
from .._pipe import pipeable, binary, binary2
from .struct import struct, nd

try:
    import numpy as np
except:
    np = Missing


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
    return np.mean(ndOrPy)

@pipeable
def std(ndOrPy, dof=0):
    # should do full numpy? std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)
    return np.std(ndOrPy, dof)

@pipeable
def sqrt(x):
    return np.sqrt(x)

@pipeable
def max(iter):
    return builtins.max(iter)

@pipeable
def min(iter):
    return builtins.min(iter)


@pipeable
def QRDecomp(A):
    Q, R = np.linalg.qr(A.nd)
    return struct(Q=nd(Q), R=nd(R))

@pipeable
def CholeskyDecomp(A):
    return nd(np.linalg.cholesky(A.nd))

@pipeable
def inv(A):
    return nd(np.linalg.inv(A.nd))


# @pipeable(flavour=binary2)
# def dot(A, B):
#     return nd(np.dot(A.nd, B.nd))
#
# @pipeable(flavour=binary2)
# def mmul(A, B):
     return nd(A.nd @ B.nd)
