# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import os, os.path
from coppertop.pipe import pipeable, unary, binary
from coppertop.pipe._pipe import Pipeable
from .string import strip
from .adverbs import each

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

