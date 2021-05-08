# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************


from .._pipe import unary1, unary


def Not(b):
    return False if b else True
Not = unary1('Not', unary, Not)
