# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable
import builtins


# conversions

@pipeable
def ToStr(x):
    return str(x)

@pipeable
def ToInt(a):
    return int(a)

@pipeable
def ToRepr(x):
    return str(x)

@pipeable
def ToString(format, x):
    raise NotImplementedError('ToString')


# other

@pipeable
def Not(x):
    return not x

@pipeable
def getAttr(x, name):
    return getattr(x, name)

@pipeable
def max(iter):
    return builtins.max(iter)

@pipeable
def min(iter):
    return builtins.min(iter)



