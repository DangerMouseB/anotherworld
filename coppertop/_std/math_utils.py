# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


try:
    import numpy
except:
    numpy = None
from .._pipe import pipeable



@pipeable
def Mean(ndOrPy):
    # should do full numpy?
    return numpy.mean(ndOrPy)

@pipeable
def Std(ndOrPy, dof=0):
    # should do full numpy? std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)
    return numpy.std(ndOrPy, dof)

@pipeable
def Sqrt(x):
    return numpy.sqrt(x)


