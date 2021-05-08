# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
# sys._ImportTrace = True   # just comment this outwhen not needed

if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)



_all = set(['Missing', 'Null', 'getMyPublicMembers', 'getPublicMembersOf', '_'])

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


from ._core import Missing, Null, ProgrammerError, PathNotTested, NotYetImplemented


# the following are wrapped in exception handlers to make testing and debugging of coppertop easier

try:
    from . import _testing, _pipe
    from ._testing import *
    _all.update(_getPublicMembersOnly(_testing))
except:
    pass

try:
    from coppertop._pipe import pipeable, nullary, unary, rau, binary, ternary, unary1, binary2, _
    _all.update(_getPublicMembersOnly(_pipe))
except:
    pass

try:
    from . import std
    from coppertop.std import *
    _all.update(_getPublicMembersOnly(std))
except:
    pass

# try:
#     from .d import stdio
#     from coppertop.d.stdio import *
#     _all.update(_getPublicMembersOnly(stdio))
# except:
#     pass

try:
    from . import range_interfaces
    from .range_interfaces import *
    _all.update(_getPublicMembersOnly(range_interfaces))
except:
    pass

try:
    from . import ranges
    from .ranges import *
    _all.update(_getPublicMembersOnly(ranges))
except:
    pass


_all =list(_all)
_all.sort()
__all__ = _all
