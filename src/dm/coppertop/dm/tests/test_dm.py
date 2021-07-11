# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************


from coppertop.bits import pipeable
from coppertop.std import assertEquals
from coppertop.dm.misc import sequence
from coppertop.dm.pmf import normalise
from coppertop.dm.utils import formatStruct


def test_misc():
    sequence(1, 10) >> assertEquals >> [1,2,3,4,5,6,7,8,9,10]


def main():
    test_misc()
    print('pass')


if __name__ == '__main__':
    main()

