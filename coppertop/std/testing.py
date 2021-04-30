# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


from .._pipe import pipeable, binary
from .maths import closeTo

_EPS = 7.105427357601E-15      # i.e. double precision



@pipeable(flavour=binary)
def assertEquals(actual, expected, suppressMsg=False, keepWS=False, returnResult=False, tolerance=_EPS):
    if keepWS:
        act = actual
        exp = expected
    else:
        act = actual.replace(" ", "").replace("\n", "") if isinstance(actual, (str,)) else actual
        exp = expected.replace(" ", "").replace("\n", "") if isinstance(expected, (str,)) else expected
    if isinstance(act, (int, float)) and isinstance(exp, (int, float)):
        equal = act >> closeTo(tolerance=tolerance) >> exp
    else:
        equal = act == exp
    if returnResult:
        return equal
    else:
        if not equal:
            if suppressMsg:
                raise AssertionError()
            else:
                if isinstance(actual, (str,)):
                    actual = '"' + actual + '"'
                if isinstance(expected, (str,)):
                    expected = '"' + expected + '"'
                raise AssertionError('expected %s but got %s' % (expected, actual))
        else:
            return None
