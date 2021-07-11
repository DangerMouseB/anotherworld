# *******************************************************************************
#
#    Copyright (c) 2019-2020 David Briant. All rights reserved.
#
# *******************************************************************************



from coppertop.bits import pipeable, unary1, binary2, unary, NotYetImplemented
from coppertop.range import EachFR, ChainAsSingleFR, UntilFR
from coppertop.range import materialise as _rMaterialise, IInputRange

@pipeable
def rZip(r):
    raise NotYetImplemented()

@pipeable
def rInject(r, seed, f):
    raise NotYetImplemented()

@pipeable
def rFilter(r, f):
    raise NotYetImplemented()

@pipeable
def rTakeBack(r, n):
    raise NotYetImplemented()

@pipeable
def rDropBack(r, n):
    raise NotYetImplemented()

@pipeable
def rFind(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

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

rEach = binary2('rEach', binary2, EachFR)
rChain = unary1('rChain', unary1, ChainAsSingleFR)
rUntil = binary2('rUntil', binary2, UntilFR)

@pipeable
def replaceWith(haystack, needle, replacement):
    return haystack >> rEach >> (lambda e: replacement if e == needle else e)

dict_keys = type({}.keys())
dict_values = type({}.values())
def materialise(x):
    if isinstance(x, dict_keys):
        return list(x)
    elif isinstance(x, IInputRange):
        return _rMaterialise(x)
    else:
        raise NotYetImplemented()
materialise = unary1('materialise', unary, materialise)
