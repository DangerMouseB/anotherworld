# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************


from coppertop import PathNotTested

def pathNotTested():
    raise PathNotTested()

class UnaryFn(object):
    def __init__(unary, fn, numArgs):
        unary.fn = fn
        unary.numArgs = numArgs
    def __call__(unary, *args, **kwargs):
        totalArgs = len(args) + len(kwargs)
        if totalArgs > unary.numArgs:
            raise SyntaxError('too many args')
        elif totalArgs < unary.numArgs:
            raise SyntaxError('too few args')
        else:
            if ... not in args:
                return unary.fn(*args, **kwargs)
            else:
                return DeferredUF(unary, args.index(...), *args, **kwargs)
    def __rrshift__(unary, arg):
        if unary.numArgs == 1:
            return unary.fn(arg)
        else:
            raise SyntaxError('too few args')

class DeferredUF(object):
    def __init__(df, uf, iArg, *args, **kwargs):
        df.uf = uf
        df.args = list(args)
        df.kwargs = kwargs
        df.iArg = iArg
    def __rrshift__(df, arg):
        df.args[df.iArg] = arg
        return df.uf.fn(*df.args, **df.kwargs)


def to(x, t):
    if t is list: return list(x)
    if t is tuple: return tuple(x)
to = UnaryFn(to, 2)


def replaceAll(xs, old, new):
    assert isinstance(xs, tuple)
    return (new if x == old else x for x in xs)
replaceAll = UnaryFn(replaceAll, 3)


def indexesOf(xs, x):
    answer = []
    for i, e in enumerate(xs):
        if x == e:
            answer.append(i)
    return answer
indexesOf = UnaryFn(indexesOf, 2)


def count(xs):
    return len(xs)
count = UnaryFn(count, 1)


def atPut(xs, iOrIs, yOrYs):
    # immutable
    xs = list(xs)
    if isinstance(iOrIs, (list, tuple)):
        for fromI, toI in enumerate(iOrIs):
            xs[toI] = yOrYs[fromI]
    else:
        xs[iOrIs] = yOrYs
    if isinstance(xs, tuple):
        return tuple(xs)
    else:
        return xs
atPut = UnaryFn(atPut, 3)


def take(xs, n):
    return xs[0:n]
take = UnaryFn(take, 2)

