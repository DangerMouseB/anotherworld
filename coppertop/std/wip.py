# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************


from .._pipe import pipeable, unary1


@pipeable(flavour=unary1)
def Not(b):
    return False if b else True

