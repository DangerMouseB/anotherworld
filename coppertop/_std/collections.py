# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable, binary


@pipeable(flavour=binary)
def join(xs, ysOrSep):
    if isinstance(ysOrSep, string):
        return sep.join(xs)
    elif isinstance(ysOrSep, (string, list)):
        return xs + ysOrSep

@pipeable(flavour=binary)
def merge(d1, d2):
    answer = dict(d1)
    answer.update(d2)
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

