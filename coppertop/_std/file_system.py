# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


import os, os.path
from .._pipe import pipeable, Pipeable, unary, binary

getCwd = os.getcwd
isFile = Pipeable('isFile', unary, os.path.isfile)
isDir = Pipeable('isDir', unary, os.path.isdir)
dirEntries = Pipeable('dirEntries', unary, os.listdir)

@pipeable(flavour=binary)
def joinPath(a, b):
    return os.path.join(a, *(b if isinstance(b, (list, tuple)) else [b]))

@pipeable
def readlines(f):
    return f.readlines()
