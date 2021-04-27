# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


import itertools, builtins
from coppertop.fp import pipeable, binary, ternary

_EPS = 7.105427357601E-15      # i.e. double precision


@pipeable(flavour=binary)
def copyTo(src, dest):
    pass



@pipeable(flavour=ternary)
def eachBoth(xs, fn2, ys):
    return [fn2(x, y) for (x, y) in zip(xs, ys)]

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
def within(x, a, b):
    # answers true if x is in the closed interval [a, b]
    return (a <= x) and (x <= b)

@pipeable
def assertEquals(actual, expected, suppressMsg=False, keepWS=False, returnResult=False, tolerance=_EPS):
    if keepWS:
        act = actual
        exp = expected
    else:
        act = actual.replace(" ", "").replace("\n", "") if isinstance(actual, (str,)) else actual
        exp = expected.replace(" ", "").replace("\n", "") if isinstance(expected, (str,)) else expected
    if isinstance(act, (int, float)) and isinstance(exp, (int, float)):
        equal = act >> closeTo(tolerance=tolerance) >> exp
    else:
        equal = act == exp
    if returnResult:
        return equal
    else:
        if not equal:
            if suppressMsg:
                raise AssertionError()
            else:
                if isinstance(actual, (str,)):
                    actual = '"' + actual + '"'
                if isinstance(expected, (str,)):
                    expected = '"' + expected + '"'
                raise AssertionError('expected %s but got %s' % (expected, actual))
        else:
            return None

@pipeable
def closeTo(a, b, tolerance=_EPS):
    if abs(a) < tolerance:
        return abs(b) < tolerance
    else:
        return abs(a - b) / abs(a) < tolerance

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