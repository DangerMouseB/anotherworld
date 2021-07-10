# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
# sys._ImportTrace = True   # just comment this outwhen not needed

if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)



_all = set(['Missing', 'Null', 'Err', 'getMyPublicMembers', 'getPublicMembersOf'])

import inspect
from . import _skip

def getMyPublicMembers(moduleName, globals, locals):
    pass

def getPublicMembersOf(module):
    pass

def _getPublicMembersOnly(module):
    def _isInOrIsChildOf(name, names):
        for parentName in names:
            if name[0:len(parentName)] == parentName:
                return True
        return False
    names = ['coppertop.flavoured', module.__name__]
    members = [(name, o) for (name, o) in inspect.getmembers(module) if (name[0:1] != '_')]         # remove private
    members = [(name, o) for (name, o) in members if not (inspect.isbuiltin(o) or inspect.ismodule(o))]   # remove built-ins and modules
    members = [(name, o) for (name, o) in members if _isInOrIsChildOf(o.__module__, names)]   # keep all pipeables and children
    return [name for (name, o) in members]


from ._core import Missing, Null, Err, ProgrammerError, UnhappyWomble, PathNotTested, NotYetImplemented


# the following are wrapped in exception handlers to make test driven development and debugging of coppertop easier

try:
    from . import _testing
    from ._testing import *
    _all.update(_getPublicMembersOnly(_testing))
except:
    pass

try:
    from coppertop_.pipe import pipeable, nullary, unary, rau, binary, ternary, unary1, binary2
    _all.update(['pipeable', 'nullary', 'unary', 'rau', 'binary', 'ternary', 'unary1', 'binary2'])
except:
    pass

try:
    from . import _repl
    from ._repl import *
    _all.update(_getPublicMembersOnly(_repl))
except:
    pass

try:
    from . import ranges
    from coppertop_.ranges._ranges import *
    _all.update(_getPublicMembersOnly(_ranges))
except:
    pass


_all =list(_all)
_all.sort()
__all__ = _all


if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__ + ' - done')