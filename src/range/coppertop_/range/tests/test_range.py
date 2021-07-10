# *******************************************************************************
#
#    Copyright (c) 2019-2020 David Briant
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



from coppertop.std import assertEquals, rEach, materialise, rChain, take
from coppertop.ranges._ranges import IndexableFR, ListOR, getIRIter


def test_listRanges():
    r = IndexableFR([1,2,3])
    o = ListOR([])
    while not r.empty:
        o.put(r.front)
        r.popFront()
    r.indexable >> assertEquals >> o.list

def test_rangeOrRanges():
    rOfR = [] >> rChain
    [e for e in rOfR >> getIRIter] >> assertEquals >> []
    rOfR = (IndexableFR([]), IndexableFR([])) >> rChain
    [e for e in rOfR >> getIRIter] >> assertEquals >> []
    rOfR = (IndexableFR([1]), IndexableFR([2])) >> rChain
    [e for e in rOfR >> getIRIter] >> assertEquals >> [1,2]

def test_other():
    [1, 2, 3] >> rEach >> (lambda x: x) >> materialise >> assertEquals >> [1, 2, 3]

def test_take():
    r1 = IndexableFR([1,2,3])
    r2 = r1 >> take(_, 3)
    r1.popFront >> assertEquals >> 1
    r3 = r1 >> take(_, 4)
    r2 >> materialise >> assertEquals >> [1,2,3]
    r3 >> materialise >> assertEquals >> [2,3]


def main():
    test_listRanges()
    test_rangeOrRanges()
    test_other()
    test_take()
    print('pass')


if __name__ == '__main__':
    main()


