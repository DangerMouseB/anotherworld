# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from pprint import pprint
from copy import copy


_list_iter_type = type(iter([]))
_numpy = None        # don't import numpy proactively


class _callFReturnX(object):
    def __init__(self, f2, pp):
        self.f2 = f2
        self.f1 = lambda x:x
        self.pp = pp
    def __rrshift__(self, other):   # other >> self
        "ENT"
        self.f2(self.f1(other))
        self.f1 = lambda x: x
        return other
    def __call__(self, f1):
        "ENT"
        self.f1 = f1
        return self
    def __lshift__(self, other):    # self << other
        "ENT"
        self.f2(self.f1(other))
        self.f1 = lambda x: x
        return self
    def __repr__(self):
        return self.pp


def _printRepr(x):
    print(repr(x))
RR = _callFReturnX(_printRepr, 'RR')

def _printStr(x):
    print(str(x))
PP = _callFReturnX(_printStr, 'PP')

def _printDir(x):
    print(dir(x))
DD = _callFReturnX(_printDir, 'DD')

def _printHelp(x):
    if hasattr(x, '_doc'):
        print(x._doc)
    else:
        help(x)
HH = _callFReturnX(_printHelp, 'HH')

def _printType(x):
    print(type(x))
TT = _callFReturnX(_printType, 'TT')

def _isNdArray(x):
    global _numpy
    if type(x).__name__ != "ndarray":
        return False
    try:
        import numpy as _numpy
        return isinstance(x, _numpy.ndarray)
    except (ModuleNotFoundError, AttributeError):      # cf None.ndarray if numpy is not installed
        return False

def _printLen(x):
    if isinstance(x, _list_iter_type):
        x = list(copy(x))
    if _isNdArray(x):
        print(x.shape)
    else:
        print(len(x))

LL = _callFReturnX(_printLen, 'LL')

