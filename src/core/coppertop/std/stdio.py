# *******************************************************************************
#
#    Copyright (c) 2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


class OStreamWrapper(object):
    def __init__(self, sGetter):
        self._sGetter = sGetter
    def __lshift__(self, other):
        # self << other
        self._sGetter().write(other)      # done as a function call so it plays nicely with HookStdOutErrToLines
        return self


cout = OStreamWrapper(lambda : sys.stdout)
cerr = OStreamWrapper(lambda : sys.stderr)

