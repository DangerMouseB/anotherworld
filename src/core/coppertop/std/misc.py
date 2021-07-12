# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.bits import NotYetImplemented
from coppertop.pipe import pipeable, unary1, unary
from coppertop.pipe._pipe import Pipeable
from .adverbs import inject


_ = ...

@pipeable
def getAttr(x, name):
    return getattr(x, name)


dict_keys = type({}.keys())
dict_values = type({}.values())
def materialise(x):
    if isinstance(x, (dict_keys, dict_values)):
        return list(x)
    else:
        raise NotYetImplemented()
materialise = unary1('materialise', unary, materialise)


def anon(func):
    return Pipeable('anon', unary, func)


@pipeable
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

