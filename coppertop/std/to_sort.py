

from .._pipe import pipeable

@pipeable
def rPushInto(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

@pipeable
def pullFrom(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return None

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
def rTake(r, n):
    raise NotImplementedError()

@pipeable
def rTakeBack(r, n):
    raise NotImplementedError()

@pipeable
def rDrop(r, n):
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

@pipeable
def rPut(r, x):
    return r.put(x)

@pipeable
def rFront(r):
    return r.front

@pipeable
def rBack(r):
    return r.back

@pipeable
def empty(r):
    return r.empty

@pipeable
def popFront(r):
    r.popFront()
    return r

@pipeable
def popBack(r):
    r.popBack()
    return r


# @pipeable
# def EachArgs(listOfArgs, f):
#     """eachArgs(f, listOfArgs)
#     Answers [f(*args) for args in listOfArgs]"""
#     return [f(*args) for args in listOfArgs]