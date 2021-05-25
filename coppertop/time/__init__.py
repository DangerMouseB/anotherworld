# *******************************************************************************
#
#    Copyright (c) 2020 David Briant. All rights reserved.
#
# *******************************************************************************

from __future__ import annotations

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


_all = set()

import inspect

def _getPublicMembersOnly(module):
    names = ['coppertop.pipeable', module.__name__]
    members = [(name, o) for (name, o) in inspect.getmembers(module) if (name[0:1] != '_')]
    members = [(name, o) for (name, o) in members if not (inspect.isbuiltin(o) or inspect.ismodule(o))]
    members = [(name, o) for (name, o) in members if (o.__module__ in names)]
    return [name for (name, o) in members]


# the following are wrapped in exception handlers to make testing and debugging of coppertop easier

try:
    from . import _enums
    from ._enums import *
    _all.update(_getPublicMembersOnly(_enums))
except:
    pass

try:
    from . import _core
    from ._core import *
    _all.update(_getPublicMembersOnly(_core))
except:
    pass


_all =list(_all)
_all.sort()
__all__ = _all
