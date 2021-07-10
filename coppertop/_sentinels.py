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
