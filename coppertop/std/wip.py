# *******************************************************************************
#
#    Copyright (c) 2021 David Briant. All rights reserved.
#
# *******************************************************************************


from .._pipe import unary1


def not_(b):
    return False if b else True
not_ = unary1('not_', unary1, not_)
Not = unary1('Not', unary1, not_)