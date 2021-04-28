# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable


# Composition - could be made more efficient

@pipeable(overrideLHS=True)
def Compose(f1, f2):
    @pipeable
    def _Composed(x):
        return x >> f1 >> f2
    return _Composed

@pipeable(overrideLHS=True)
def ComposeAll(f1, f2):
    raise NotImplementedError()
