# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.pipe import pipeable, unary1


@pipeable(flavour=unary1)
def toStr(x):
    return str(x)

@pipeable(flavour=unary1)
def toInt(a):
    return int(a)

@pipeable(flavour=unary1)
def toRepr(x):
    return str(x)

@pipeable(flavour=unary1)
def toString(format, x):
    raise NotImplementedError('ToString')

@pipeable(flavour=unary1)
def toList(x):
    return list(x)
