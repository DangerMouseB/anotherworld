# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._core import NotYetImplemented
from .._pipe import pipeable, unary1, unary, Pipeable
from .adverbs import inject
from ..ranges import materialise as _rMaterialise, IInputRange

_ = ...

@pipeable
def getAttr(x, name):
    return getattr(x, name)


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


def anon(func):
    return Pipeable('anon', unary, func)


@pipeable
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

