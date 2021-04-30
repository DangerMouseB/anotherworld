# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys

if not hasattr(sys, '_Missing'):
    class Missing(object):
        def __bool__(self):
            return False
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'Missing'
    sys._Missing = Missing()
Missing = sys._Missing


if not hasattr(sys, '_NULL'):
    class _NULL(object):
        # def __str__(self):
        #     return 'na'
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'Null'
    sys._NULL = _NULL()
Null = sys._NULL

class ProgrammerError(Exception): pass
class NotYetImplemented(Exception): pass
class PathNotTested(Exception): pass
