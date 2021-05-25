# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable, binary, binary2, unary1
from .struct import struct, nd
from .misc import dict_keys, dict_values
from .adverbs import rEach
from ._core import assertType


@pipeable
def wrapInList(x):
    l = list()
    l.append(x)
    return l

@pipeable
def put(r, x):
    return r.put(x)

@pipeable(flavour=unary1)
def front(r):
    return r.front

@pipeable(flavour=unary1)
def back(r):
    return r.back

@pipeable(flavour=unary1)
def empty(r):
    return r.empty

@pipeable(flavour=unary1)
def popFront(r):
    r.popFront()
    return r

@pipeable(flavour=unary1)
def popBack(r):
    r.popBack()
    return r

@pipeable
def first(x):
    raise NotImplementedError()

@pipeable
def last(x):
    raise NotImplementedError()

@pipeable
def take(x, n):
    raise NotImplementedError()

@pipeable
def drop(x, n):
    raise NotImplementedError()

@pipeable
def replaceWith(haystack, needle, replacement):
    return haystack >> rEach >> (lambda e: replacement if e == needle else e)

@pipeable
def sort(x, key=None, reverse=False):
    if isinstance(x, dict):
        return dict(sorted(x.items(), key=key, reverse=reverse))
    else:
        return sorted(x, key=key, reverse=reverse)

@pipeable(flavour=unary1)
def count(x):
    if isinstance(x, struct):
        f = next(iter(x._fields()))
        return x[f] >> count
    else:
        return len(x)

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
    assertType(a, dict)
    assertType(b, (struct, dict))
    answer = dict(a)
    if isinstance(b, struct):
        answer.update(b._fvPairs())
    else:
        answer.update(b)
    return answer

@pipeable(flavour=binary2)
def override(a, b):
    assertType(a, struct)
    assertType(b, (struct, dict))
    answer = struct(a)
    if isinstance(b, struct):
        answer._update(b._fvPairs())
    else:
        answer._update(b)
    return answer

@pipeable(flavour=binary2)
def underride(a, b):
    assertType(a, struct)
    assertType(b, (struct, dict))
    answer = struct(a)
    for k, v in (b._fvPairs() if isinstance(b, struct) else b.items()):
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
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

@pipeable
def fromto(x, s1, s2=None):
    return x[s1:s2]

@pipeable
def at(xs, iOrIs):
    if not issubclass(xs.__class__, (list, dict, tuple)):
        raise TypeError('xs must be a subclass of list, dict or tuple')
    if isinstance(iOrIs, (list, tuple)):
        answer = []
        for i in iOrIs:
            answer.append(xs[i])
        return answer
    else:
        return xs[iOrIs]

@pipeable(flavour=binary2)
def intersects(a, b):
    if not isinstance(a, (list, tuple, set, dict_keys, dict_values)):
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return a == b
        else:
            return a in b
    else:
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return b in a
        else:
            for e in a:
                if e in b:
                    return True
            return False

@pipeable(flavour=binary2)
def subsetOf(a, b):
    if not isinstance(a, (list, set, tuple, dict_keys, dict_values)):
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1, 1
            return a == b
        else:
            # 1, 1+
            return a in b
    else:
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1+, 1
            return False
        else:
            # 1+, 1+
            for e in a:
                if e not in b:
                    return False
            return True

def _where(s, bools):
    assert isinstance(s, struct)
    answer = struct(s)
    for f, v in s._fvPairs():
        answer[f] = nd(v.nd[bools.nd])
    return answer
where = binary2('where', binary, _where)


@pipeable
def rename(d, old, new):
    if isinstance(d, struct):
        d = struct(d)
        d[new] = d._pop(old)
        return d

    else:
        d = dict(d)
        d[new] = d.pop(old)
        return d


@pipeable
def replace(d, f, new):
    d = struct(d) if isinstance(d, struct) else dict(d)
    d[f] = new
    return d