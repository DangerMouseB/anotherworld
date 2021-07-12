# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
# sys._TRACE_IMPORTS = True

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


_all = set(['Missing', 'Null', 'Err', 'getMyPublicMembers', 'getPublicMembersOf'])

import inspect


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


from . _core import Missing, Null, Err, ProgrammerError, UnhappyWomble, PathNotTested, NotYetImplemented


# the following are wrapped in exception handlers to make test driven development and debugging of coppertop easier

try:
    from .testing import *
    from . import testing as _mod
    _all.update(_getPublicMembersOnly(_mod))
except:
    pass

try:
    from .pipe import pipeable, nullary, unary, rau, binary, ternary, unary1, binary2
    _all.update(['pipeable', 'nullary', 'unary', 'rau', 'binary', 'ternary', 'unary1', 'binary2'])
except:
    pass

try:
    from .utils import *
    from . import utils as _mod
    _all.update(_getPublicMembersOnly(_mod))
except:
    pass

try:
    from .repl import *
    from . import repl as _mod
    _all.update(_getPublicMembersOnly(_mod))
except:
    pass


_all =list(_all)
_all.sort()
__all__ = _all


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')

