# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************

import numpy as np
from .._core import Missing
from .._pipe import unary1, pipeable
from ._core import assertType


class struct(dict):
    def __new__(cls, _structOrDict=Missing, **kwargs):
        return super().__new__(cls)
    def __init__(s, _structOrDict=Missing, **kwargs):
        if _structOrDict is Missing:
            pass
        elif isinstance(_structOrDict, struct):
            super().update(_structOrDict._fvPairs())
        elif isinstance(_structOrDict, dict):
            super().update(_structOrDict)
        else:
            raise TypeError('first argument must be a prototype struct - got ' + repr(_structOrDict))
        super().update(kwargs)
    def __getattribute__(s, field):
        if field == '_fields':
            return super().keys
        if field == '_fvPairs':
            return super().items
        if field == '_values':
            return super().values
        if field == '_update':
            return super().update
        else:
            return super().get(field, Missing)
    def __setattr__(s, field, value):
        return super().__setitem__(field, value)
    def __getitem__(s, fieldOrFields):
        if isinstance(fieldOrFields, (list, tuple)):
            fvs = {field: s[field] for field in fieldOrFields}
            return struct(fvs)
        if fieldOrFields is ...:
            return struct(s)   # make a copy so can be updated
        else:
            return super().get(fieldOrFields, Missing)
    def __repr__(s):
        itemStrings = (f"{str(k)}={repr(v)}" for k, v in super().items())
        rep = "{}({})".format(type(s).__name__, ", ".join(itemStrings))
        return rep
    # def __eq__(self, other):
    #     return self.__dict__ == other.__dict__



@pipeable(flavour=unary1)
def fields(x):
    assertType(x, (struct, dict))
    if isinstance(x, struct):
        return x._fields()
    else:
        raise x.keys()

@pipeable(flavour=unary1)
def fvPairs(x):
    assertType(x, (struct, dict))
    if isinstance(x, struct):
        return x._fvPairs()
    else:
        return x.items()

@pipeable(flavour=unary1)
def values(x):
    assertType(x, (struct, dict))
    if isinstance(x, struct):
        return x._values()
    else:
        return x.values()


@pipeable(flavour=unary1)
def nd(x):
    return _nd(x)

class _nd(object):
    def __init__(self, x):
        if isinstance(x, np.ndarray):
            self.nd = x
        else:
            self.nd = np.array(x)
    def __add__(self, other):
        return nd(self.nd + (other.nd if isinstance(other, _nd) else other))
    def __mul__(self, other):
        return nd(self.nd * (other.nd if isinstance(other, _nd) else other))
    def __lt__(self, other):
        return nd(self.nd < (other.nd if isinstance(other, _nd) else other))
    def __gt__(self, other):
        return nd(self.nd > (other.nd if isinstance(other, _nd) else other))
    def __and__(self, other):
        return nd(self.nd & (other.nd if isinstance(other, _nd) else other))
    def __repr__(self):
        return repr(self.nd)
    def __rrshift__(self, other):
        return repr(self.nd)