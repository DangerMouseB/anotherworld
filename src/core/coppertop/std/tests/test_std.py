# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************


import operator
from coppertop.std import assertEquals, _, inject, each, eachAsArgs
from coppertop.pipe import pipeable


def test_adverbs():
    from coppertop.std.adverbs import _test_inject
    _test_inject()


def test_stuff():
    2 >> assertEquals >> 2

    @pipeable
    def squareIt(x):
        return x * x

    @pipeable
    def add(x, y):
        return x + y

    [1,2,3] >> each >> squareIt >> inject(_, 0, _) >> add >> assertEquals >> 14

    [[1,2], [2,3], [3,4]] >> eachAsArgs >> add >> assertEquals >> [3, 5, 7]
    [[1, 2], [2, 3], [3, 4]] >> eachAsArgs >> operator.add >> assertEquals >> [3, 5, 7]


def main():
    test_adverbs()
    test_stuff()
    print('pass')


if __name__ == '__main__':
    main()

