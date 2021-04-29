# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


import os, os.path
from .._pipe import pipeable, Pipeable, unary, binary
from .string import strip
from .iteration import each

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

@pipeable
def linesOf(pathfilename):
    with open(pathfilename) as f:
        return f >> readlines >> each >> strip(...,'\\n')

@pipeable(flavour=binary)
def copyTo(src, dest):
    raise NotImplementedError()


