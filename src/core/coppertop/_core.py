# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


def ensureSingletons():
    # These are kept on sys so their identity isn't changed on reload (a frequent
    # occurrence in Jupyter)


    # error sentinels - cf missing, null, nan in databases

    # something should / could be there but it is definitely not there
    if not hasattr(sys, '_Missing'):
        class Missing(object):
            def __bool__(self):
                return False
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Missing'
        sys._Missing = Missing()

    # the null set
    if not hasattr(sys, '_NULL'):
        class _NULL(object):
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Null'
        sys._NULL = _NULL()

    # general error
    if not hasattr(sys, '_ERR'):
        class _ERR(object):
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Err'
        sys._ERR = _ERR()

    # not a - e.g. not a number, not a date, etc #NA!, #NUM!, #VALUE!
    # np.log(0)  => -inf, #np.log(-1)  => nan, tbd


    # general exceptions

    if not hasattr(sys, '_ProgrammerError'):
        class ProgrammerError(Exception): pass
        sys._ProgrammerError = ProgrammerError

    if not hasattr(sys, '_NotYetImplemented'):
        class NotYetImplemented(Exception): pass
        sys._NotYetImplemented = NotYetImplemented

    if not hasattr(sys, '_PathNotTested'):
        class PathNotTested(Exception): pass
        sys._PathNotTested = PathNotTested

    if not hasattr(sys, '_UnhappyWomble'):
        class UnhappyWomble(Exception): pass
        sys._UnhappyWomble = UnhappyWomble

ensureSingletons()

Missing = sys._Missing
Null = sys._NULL
Err = sys._ERR
ProgrammerError = sys._ProgrammerError
NotYetImplemented = sys._NotYetImplemented
PathNotTested = sys._PathNotTested
UnhappyWomble = sys._UnhappyWomble

