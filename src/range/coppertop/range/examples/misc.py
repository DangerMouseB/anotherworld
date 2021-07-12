# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


class Fred(object):
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return 'rep(%s)' % self.x
    def __str__(self):
        return 'str(%s)' % self.x