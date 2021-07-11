# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from typing import Iterable
import numpy
from coppertop.bits import Missing
from coppertop.pipe import unary1, pipeable
from ._core import assertType


class struct(dict):
    # mutable when using a regular python style
    # may be later wrapped in an immutable accessor
    def __new__(cls, _structOrDict=Missing, **kwargs):
        return super().__new__(cls)
    def __init__(s, _structOrDict=Missing, **kwargs):
        if _structOrDict is Missing:
            pass
        elif isinstance(_structOrDict, struct):
            super().update(_structOrDict._pairsForTreeCopy)
        elif isinstance(_structOrDict, (dict, list, tuple)):
            super().update(_structOrDict)
        else:
            raise TypeError('first argument must be a prototype struct - got ' + repr(_structOrDict))
        super().update(kwargs)
    def __dir__(s) -> Iterable[str]:
        answer = list(super().keys())
        return answer
    def __getattribute__(s, field):
        # print(field)
        if field[0:2] == '__':
            if field == '__class__':
                return struct
            raise AttributeError()
        elif field[0:1] == "_":
            if field == '_fields':
                return super().keys
            if field == '_fvPairs':
                return super().items
            if field == '_pairsForTreeCopy':
                # in collaboration with __new__ this will recursively answer a tree
                # copy (deep copy breaking diamonds) of any structs but not other
                # objects (which will be shared / aliased). will go into an infinite
                # loop on cycles (which we don't and shouldn't allow but nonetheless
                # we should raise an error for, i.e. need to detect them - tbd)
                answer = {}
                for k,v in super().items():
                    if issubclass(v.__class__, struct):
                        answer[k] = v.__class__(v)
                    else:
                        answer[k] = v
                return answer
            if field == '_values':
                return super().values
            if field == '_pop':
                return super().pop
            if field == '_update':
                return super().update
            if field == '_setdefault':
                return super().setdefault
            if field == '_get':
                return super().get
            return super().get(field[1:], Missing)
        else:
            if field == 'items':
                # for pycharm :(   - pycharm knows we are a subclass of dict so is inspecting us via items
                # longer term we may return a BTStruct instead of struct in response to __class__
                return {}.items
            try:
                return super().__getitem__(field)
            except KeyError:
                raise AttributeError(f"'struct' object has no attribute '{field}'")
    def __setattr__(s, field, value):
        return super().__setitem__(field, value)
    def __call__(s, **kwargs):
        for field, value in kwargs.items():
            super().__setitem__(field, value)
        return s
    def __getitem__(s, fieldOrFields):
        if isinstance(fieldOrFields, (list, tuple)):
            fvs = {field: s[field] for field in fieldOrFields}
            return struct(fvs)
        return super().__getitem__(fieldOrFields)
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
        return x.keys()

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
        if isinstance(x, numpy.ndarray):
            self.nd = x
        else:
            self.nd = numpy.array(x)

    @property
    def T(self):
        return nd(self.nd.T)

    @property
    def conj(self):
        return nd(self.nd.conj())

    def __add__(self, other):
        return nd(self.nd + (other.nd if isinstance(other, _nd) else other))
    def __radd__(self, other):
        return nd((other.nd if isinstance(other, _nd) else other) + self.nd)

    def __sub__(self, other):
        return nd(self.nd - (other.nd if isinstance(other, _nd) else other))
    def __rsub__(self, other):
        return nd((other.nd if isinstance(other, _nd) else other) - self.nd)

    def __mul__(self, other):
        return nd(self.nd * (other.nd if isinstance(other, _nd) else other))
    def __rmul__(self, other):
        return nd((other.nd if isinstance(other, _nd) else other) * self.nd)

    def __truediv__(self, other):
        return nd(self.nd / (other.nd if isinstance(other, _nd) else other))
    def __rtruediv__(self, other):
        return nd((other.nd if isinstance(other, _nd) else other) / self.nd)

    def __matmul__(self, other):
        return nd(self.nd @ (other.nd if isinstance(other, _nd) else other))
    def __rmatmul__(self, other):
        return nd((other.nd if isinstance(other, _nd) else other) @ self.nd)

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