# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable

@pipeable
def PushInto(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

@pipeable
def PullFrom(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return None

@pipeable
def RZip(r):
    raise NotImplementedError()

@pipeable
def RFold(r, f):
    raise NotImplementedError()

@pipeable
def RFoldSeed(seed, r, f):
    raise NotImplementedError()

@pipeable
def RFilter(r, f):
    raise NotImplementedError()

@pipeable
def RTake(r, n):
    raise NotImplementedError()

@pipeable
def RTakeBack(r, n):
    raise NotImplementedError()

@pipeable
def RDrop(r, n):
    raise NotImplementedError()

@pipeable
def RDropBack(r, n):
    raise NotImplementedError()

@pipeable
def Find(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

@pipeable
def Put(r, x):
    return r.put(x)

@pipeable
def Front(r):
    return r.front

@pipeable
def Back(r):
    return r.back

@pipeable
def Length(r):
    return r.length

@pipeable
def Empty(r):
    return r.empty

@pipeable
def PopFront(r):
    r.popFront()
    return r

@pipeable
def PopBack(r):
    r.popBack()
    return r
