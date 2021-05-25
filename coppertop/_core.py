# *******************************************************************************
#
#    Copyright (c) 2011-2021 David Briant. All rights reserved.
#
# *******************************************************************************


# error sentinels - cf missing, null, nan in databases

# we keep them on sys so their identity isn't changed on reload (a frequent
# occurrence in Jupyter)
import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


# something should / could be there but it is missing
if not hasattr(sys, '_Missing'):
    class Missing(object):
        def __bool__(self):
            return False
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'Missing'
    sys._Missing = Missing()
Missing = sys._Missing


# the null set
if not hasattr(sys, '_NULL'):
    class _NULL(object):
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'Null'
    sys._NULL = _NULL()
Null = sys._NULL


# general error
if not hasattr(sys, '_ERR'):
    class _ERR(object):
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'Err'
    sys._ERR = _ERR()
Err = sys._ERR


# not a - e.g. not a number, not a date, etc #NA!, #NUM!, #VALUE!
# np.log(0)  => -inf, #np.log(-1)  => nan, tbd



class ProgrammerError(Exception): pass
class UnhappyWomble(Exception): pass
class NotYetImplemented(Exception): pass
class PathNotTested(Exception): pass

