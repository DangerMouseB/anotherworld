

from .._pipe import pipeable

@pipeable
def rZip(r):
    raise NotImplementedError()

@pipeable
def rInject(r, seed, f):
    raise NotImplementedError()

@pipeable
def rFilter(r, f):
    raise NotImplementedError()

@pipeable
def rTakeBack(r, n):
    raise NotImplementedError()

@pipeable
def rDropBack(r, n):
    raise NotImplementedError()

@pipeable
def rFind(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r


