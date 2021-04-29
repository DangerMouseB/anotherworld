# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


import itertools, builtins
from .._pipe import pipeable, binary
from .._core import Missing





@pipeable
def Not(b):
    return False if b else True



