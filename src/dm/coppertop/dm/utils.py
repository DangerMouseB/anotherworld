# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************


from coppertop.bits import pipeable
from coppertop.std import fvPairs, each, join

@pipeable
def formatStruct(s, name, keysFormat, valuesFormat, sep):
    def formatKv(kv):
        k,v = kv
        k = k if isinstance(k, str) else format(k, keysFormat)
        v = v if isinstance(v, str) else format(v, valuesFormat)
        return f'{k}={v}'
    return f'{name}({s >> fvPairs >> each >> formatKv >> join >> sep})'

