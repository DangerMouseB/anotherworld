# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# *******************************************************************************


import operator
from coppertop.std import assertEquals, _, inject, each, eachAsArgs
from coppertop import pipeable


def test_adverbs():
    from ..std.adverbs import _test_inject
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

