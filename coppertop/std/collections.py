# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable, binary, binary2
from .struct import struct
from ._core import assertType


@pipeable
def sort(x, key=None, reverse=False):
    if isinstance(x, dict):
        return dict(sorted(x.items(), key=key, reverse=reverse))
    else:
        return sorted(x, key=key, reverse=reverse)

@pipeable
def count(iter):
    return len(iter)

@pipeable(flavour=binary2)
def join(xs, ysOrSep):
    if isinstance(ysOrSep, str):
        return ysOrSep.join(xs)
    elif isinstance(ysOrSep, (tuple, list)):
        return xs + ysOrSep
    else:
        raise TypeError()

@pipeable(flavour=binary2)
def merge(a, b):
    assertType(a, (struct, dict))
    assertType(b, (struct, dict))
    if isinstance(a, struct):
        answer = struct(a)
        if isinstance(b, struct):
            answer._update(b._fvPairs())
        else:
            answer._update(b)
    else:
        answer = dict(a)
        if isinstance(b, struct):
            answer.update(b._fvPairs())
        else:
            answer.update(b)
    return answer

@pipeable
def replaceAll(xs, old, new):
    assert isinstance(xs, tuple)
    return (new if x == old else x for x in xs)

@pipeable
def indexesOf(xs, x):
    answer = []
    for i, e in enumerate(xs):
        if x == e:
            answer.append(i)
    return answer

@pipeable
def atPut(xs, iOrIs, yOrYs):
    # immutable
    if not isinstance(xs, list):
        raise TypeError('xs must be a list')
    xs = list(xs)
    if isinstance(iOrIs, (list, tuple)):
        for fromI, toI in enumerate(iOrIs):
            xs[toI] = yOrYs[fromI]
    else:
        xs[iOrIs] = yOrYs
    return xs

@pipeable(flavour=binary2)
def intersects(a, b):
    if not isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)):
            return a == b
        else:
            return a in b
    else:
        if not isinstance(b, (list, tuple)):
            return b in a
        else:
            for e in a:
                if e in b:
                    return True
            return False

@pipeable(flavour=binary2)
def subsetOf(a, b):
    if not isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)):
            # 1, 1
            return a == b
        else:
            # 1, 1+
            return a in b
    else:
        if not isinstance(b, (list, tuple)):
            # 1+, 1
            return False
        else:
            # 1+, 1+
            for e in a:
                if e not in b:
                    return False
            return True

