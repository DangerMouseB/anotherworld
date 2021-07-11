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
    from . import testing
    from .testing import *
    _all.update(_getPublicMembersOnly(testing))
except:
    pass

try:
    from .pipe import pipeable, nullary, unary, rau, binary, ternary, unary1, binary2
    _all.update(['pipeable', 'nullary', 'unary', 'rau', 'binary', 'ternary', 'unary1', 'binary2'])
except:
    pass

try:
    from . import repl
    from .repl import *
    _all.update(_getPublicMembersOnly(repl))
except:
    pass

# try:
#     import coppertop.range
#     from coppertop.range._range import *
#     _all.update(_getPublicMembersOnly(coppertop.range))
# except:
#     pass


_all =list(_all)
_all.sort()
__all__ = _all


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')