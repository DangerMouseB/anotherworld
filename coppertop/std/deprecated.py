# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************


from coppertop import pipeable


@pipeable
def toStr(x):
    return str(x)

@pipeable
def toInt(a):
    return int(a)

@pipeable
def toRepr(x):
    return str(x)

@pipeable
def toString(format, x):
    raise NotImplementedError('ToString')

