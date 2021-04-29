# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable
# from ..ranges import RMap



@pipeable
def WrapInList(x):
    l = []
    l.append(x)
    return l

@pipeable
def First(x):
    raise NotImplementedError()

@pipeable
def Last(x):
    raise NotImplementedError()

@pipeable
def Take(x):
    raise NotImplementedError()

@pipeable
def Cut(x):
    raise NotImplementedError()

@pipeable
def ReplaceWith(haystack, needle, replacement):
    return haystack >> RMap >> (lambda e: replacement if e == needle else e)


