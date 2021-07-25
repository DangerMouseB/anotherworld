# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import inspect, types
from coppertop._singletons import ProgrammerError, NotYetImplemented


class _DeferredArg():
    def __repr__(self):
        return '...'
DeferredArg = _DeferredArg()


class Pipeable(object):
    def __init__(p, name, flavour, fn):
        p.name = name
        p.flavour = flavour
        p.fn = fn

    def __call__(p, *args, **kwargs):
        "ENT"
        return p.flavour(p, False, args >> substituteEllipses, kwargs)

    def __rrshift__(p, arg):  # arg >> p
        "ENT"
        if p.flavour.numLeft == 0:
            raise SyntaxError(f'arg >> {p.name} - illegal syntax for a {p.flavour.name}')
        else:
            args = [DeferredArg] * p.flavour.numPiped
            df = p.flavour(p, False, args, {})
            return df.__rrshift__(arg)

    def __rshift__(p, arg):  # p >> arg
        "ENT"
        if p.flavour.numLeft == 0 and p.flavour.numRight > 0:
            # only rau can handle this case
            args = [DeferredArg] * p.flavour.numRight
            df = p.flavour(p, False, args, {})
            return df.__rshift__(arg)
        else:
            if hasattr(arg, '__rrshift__'):
                try:
                    arg.__rrshift__(p)
                except:
                    return NotImplemented
            else:
                raise SyntaxError(f'{p.name} >> arg - illegal syntax for a {p.flavour.name}')

    def __repr__(p):
        return p.name

    def dispatch(p, args, kwargs):
         return p.fn(*args, **kwargs)


class PartialCall(object):

    def __new__(cls, p, isPiping, args, kwargs):
        syntaxErrIf(count(args) < cls.numPiped, f'needs at least {cls.numPiped} arg' + pluraliseIf(cls.numPiped > 1))
        if not (iDefArgs := args >> indexesOf(..., DeferredArg)):
            return p.dispatch(args, kwargs)
        else:
            pc = super().__new__(cls)
            pc.p = p
            pc.args = args
            pc.kwargs = kwargs
            pc.iDefArgs = iDefArgs
            pc.isPiping = isPiping
            return pc

    def __call__(pc, *args, **kwargs):
        "ENT"
        syntaxErrIf(pc.isPiping, f'syntax not of form {prettyForm(pc.__class__)}')
        syntaxErrIf(count(args) > count(pc.iDefArgs), f'{pc.p.name} - too many args - got {count(args)} needed {count(pc.iDefArgs)}')
        newArgs = pc.args >> atPut(..., pc.iDefArgs[0:count(args)], args >> substituteEllipses)
        newKwargs = override(pc.kwargs, kwargs)
        return pc.__class__(pc.p, pc.isPiping, newArgs, newKwargs)

    def __rrshift__(pc, arg):  # arg >> pc
        "ENT"
        if pc.numLeft == 0:
            # if we are here then the arg does not implement __rshift__ so this is a syntax error
            syntaxErrIf(True, f'syntax not of form {prettyForm(pc.__class__)}')
        else:
            syntaxErrIf(pc.isPiping, f'syntax not of form {prettyForm(pc.__class__)}')
            syntaxErrIf(count(pc.iDefArgs) != pc.numPiped,
                         f'needs {count(pc.iDefArgs)} args but {pc.numPiped} will be piped')
            newArgs = pc.args >> atPut(..., pc.iDefArgs, [arg] + [DeferredArg] * (pc.numPiped - 1))
            return pc.__class__(pc.p, True, newArgs, pc.kwargs)

    def __rshift__(pc, arg):  # pc >> arg
        "ENT"
        if pc.numRight == 0:
            return NotImplemented
        else:
            if isinstance(pc, rau):
                if isinstance(arg, Pipeable):
                    if arg.flavour in (nullary, unary, binary, ternary):
                        raise TypeError(f'we don\'t  allow a rau to consume a unary, binary, adverb or binaryAdverb')
                    if arg.flavour == rau:
                        raise NotYetImplemented('could make sense...')
                syntaxErrIf(count(pc.iDefArgs) != pc.numPiped,
                             f'needs {count(pc.iDefArgs)} args but {pc.numPiped} will be piped')
                newArgs = pc.args >> atPut(..., pc.iDefArgs[0], arg)
            elif isinstance(pc, binary):
                syntaxErrIf(not pc.isPiping, f'syntax not of form {prettyForm(pc.__class__)}')
                newArgs = pc.args >> atPut(..., pc.iDefArgs[0], arg)
            elif isinstance(pc, ternary):
                syntaxErrIf(not pc.isPiping, f'syntax not of form {prettyForm(pc.__class__)}')
                if count(pc.iDefArgs) == 2:
                    newArgs = pc.args >> atPut(..., pc.iDefArgs[0:2], [arg, DeferredArg])
                elif count(pc.iDefArgs) == 1:
                    newArgs = pc.args >> atPut(..., pc.iDefArgs[0], arg)
                else:
                    raise ProgrammerError()
            else:
                raise ProgrammerError()
            return pc.__class__(pc.p, True, newArgs, pc.kwargs)

    def __repr__(pc):
        return f"{pc.p.name}({', '.join([repr(arg) for arg in pc.args])})"


class nullary(PartialCall):
    name = 'nullary'
    numPiped = 0
    numLeft = 0
    numRight = 0


class unary(PartialCall):
    name = 'unary'
    numPiped = 1
    numLeft = 1
    numRight = 0


class rau(PartialCall):
    name = 'rau'
    numPiped = 1
    numLeft = 0
    numRight = 1


class binary(PartialCall):
    name = 'binary'
    numPiped = 2
    numLeft = 1
    numRight = 1


class ternary(PartialCall):
    name = 'ternary'
    numPiped = 3
    numLeft = 1
    numRight = 2


class unary1(Pipeable):
    names = 'unary1'
    def __call__(p, *args, **kwargs):#@DontTrace
        "ENT"
        return p.fn(*args, **kwargs)
    def __rrshift__(p, arg): #@DontTrace # arg >> p
        "ENT"
        return p.fn(arg)


class binary2(Pipeable):
    names = 'binary2'
    def __call__(b2, *args, **kwargs):#@DontTrace
        "ENT"
        return b2.fn(*args, **kwargs)
    def __rrshift__(b2, arg1):  #@DontTrace  # arg1 >> b2
        "ENT"
        return partialBinary2(b2.fn, arg1)
class partialBinary2(object):
    def __init__(pb2, fn, arg1):#@DontTrace
        pb2.fn = fn
        pb2.arg1 = arg1
    def __rshift__(pb2, arg2):#@DontTrace  # b2 >> arg2
        "ENT"
        return pb2.fn(pb2.arg1, arg2)


def prettyForm(flavour):
    if issubclass(flavour, nullary):
        return f'{flavour.name}()'
    else:
        return \
            (f'x >> {flavour.name}' if flavour.numLeft > 0 else f'{flavour.name}') + \
            (' >> y' if flavour.numRight == 1 else '') + \
            (' >> y >> z' if flavour.numRight == 2 else '')



def syntaxErrIf(bool, desc):
    if bool: raise SyntaxError(desc)


def pluraliseIf(bool):
    return 's' if bool else ''


_I_FRAME = 0
_I_FILENAME = 1
_I_FUNCTION = 3


def pipeable(*args, flavour=unary):

    def registerFn(fn):
        if isinstance(fn, type):
            # class
            pass
            # raise TypeError(f'Can\'t wrap classes - "{fn.__name__}"')

        # function
        # _ret = inspect.signature(fn).return_annotation
        # argNames = []
        # argTypes = []
        # for pName, parameter in inspect.signature(fn).parameters.items():
        #     if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
        #         raise TypeError('Function must not include *%s' % pName)
        #     elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
        #         raise TypeError('Function must not include **%s' % pName)
        #     else:
        #         if parameter.default == inspect.Parameter.empty:
        #             argNames += [pName]
        #             argTypes += [parameter.annotation]
        #         else:
        #             raise TypeError('Function must not include %s=%s' % (pName, parameter.default))
        # _sig = tuple(argTypes)
        # # _sig = tuple(bhash(e) for e in _sig)
        # for argType, argName in zip(_sig, argNames):
        #     if argType is inspect._empty:
        #         pass
        #         #raise TypeError(f'No type for "{argName}" for function "{fn.__name__}"')
        doc = fn.__doc__ if hasattr(fn, '__doc__') else ''
        _name = fn.__name__

        # figure if a function of the same name has been imported and copy it's detailsBySig if so
        s = inspect.stack()
        if (s[1].function != '<module>') and (s[1].function != 'bones'):
            pass
            # raise SyntaxError('@bones is only allowed on module level functions')
        iModule = -1
        for i in range(3):
            if s[i][_I_FUNCTION] == '<module>':
                iModule = i
                break
        # if iModule == -1:
        #     raise SyntaxError('Can\'t find module within 2 levels')
        # module = inspect.getmodule(s[iModule][_I_FRAME])
        # moduleName = inspect.getmodulename(s[iModule][_I_FILENAME])
        # packageName = module.__package__
        #myFullModuleName = packageName + '.' + moduleName + '.' + _name

        if issubclass(flavour, Pipeable):
            mf = flavour(_name, flavour, fn)
        else:
            mf = Pipeable(_name, flavour, fn)
        return mf

    if len(args) == 1 and isinstance(args[0], (types.FunctionType, types.MethodType, type)):
        # of form @bones so args[0] is the function or class being decorated
        return registerFn(args[0])

    elif len(args) == 1 and isinstance(args[0], str):
        # of form  @bones('<typelang>')
        raise NotImplementedError()

    else:
        # of form as @bones() or @pipeable(overrideLHS=True) etc
        if len(args): raise TypeError('Only kwargs allowed')
        return registerFn


# the following is just so I can use >> above - if the above is ever slow normal python functions can be used instead

class _Unary1Fn(object):
    def __init__(unary, fn, numArgs):
        unary.fn = fn
        unary.numArgs = numArgs
    def __call__(unary, *args, **kwargs):
        return unary.fn(*args, **kwargs)
    def __rrshift__(unary, arg):
        return unary.fn(arg)

class _UnaryFn(object):
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
                return _DeferredUF(unary, args.index(...), *args, **kwargs)
    def __rrshift__(unary, arg):
        if unary.numArgs == 1:
            return unary.fn(arg)
        else:
            raise SyntaxError('too few args')

class _DeferredUF(object):
    def __init__(df, uf, iArg, *args, **kwargs):
        df.uf = uf
        df.args = list(args)
        df.kwargs = kwargs
        df.iArg = iArg
    def __rrshift__(df, arg):
        df.args[df.iArg] = arg
        return df.uf.fn(*df.args, **df.kwargs)

def override(d1, d2):
    answer = dict(d1)
    answer.update(d2)
    return answer
override = _UnaryFn(override, 2)

def count(lenable):
    return len(lenable)
count = _UnaryFn(count, 1)

def indexesOf(xs, x):
    answer = []
    for i, e in enumerate(xs):
        if x == e:
            answer.append(i)
    return answer
indexesOf = _UnaryFn(indexesOf, 2)

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
atPut = _UnaryFn(atPut, 3)

def substituteEllipses(xs):
    return tuple(DeferredArg if x is ... else x for x in xs)
substituteEllipses = _Unary1Fn(substituteEllipses, 1)

