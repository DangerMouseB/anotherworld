# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable, binary
from .._core import Missing


@pipeable(flavour=binary)
def endsWith(s1, s2):
    return s1.endswith(s2)

@pipeable(flavour=binary)
def startsWith(s1, s2):
    return s1.startswith(s2)

@pipeable
def strip(s, chars=Missing):
    if chars is Missing:
        return s.strip()
    else:
        return s.strip(chars)

@pipeable(flavour=binary)
def split(s1, s2, maxsplit=Missing):
    if maxsplit is Missing:
        return s1.split(s2)
    else:
        return s1.split(s2, maxsplit)


@pipeable
def LJust(w, s, pad=" "):
    return s.ljust(w, pad)

@pipeable
def RJust(w, s, pad=" "):
    return s.rjust(w, pad)

@pipeable
def CJust(w, s, pad=" "):
    return s.center(w, pad)

@pipeable
def Format(format, thing):
    return format.format(thing)

