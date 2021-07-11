# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


_ = ...


def assertType(x, t):
    if isinstance(x, t):
        return x
    else:
        #SHOULDDO add the name of the calling function to the error msg
        raise TypeError('got: ' + str(type(x)) + ' but expected: ' + str(t))

