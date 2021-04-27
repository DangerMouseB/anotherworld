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


import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from coppertop._pipe import pipeable

@pipeable
def PushInto(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

@pipeable
def PullFrom(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return None

@pipeable
def RZip(r):
    raise NotImplementedError()

@pipeable
def RFold(r, f):
    raise NotImplementedError()

@pipeable
def RFoldSeed(seed, r, f):
    raise NotImplementedError()

@pipeable
def RFilter(r, f):
    raise NotImplementedError()

@pipeable
def RTake(r, n):
    raise NotImplementedError()

@pipeable
def RTakeBack(r, n):
    raise NotImplementedError()

@pipeable
def RDrop(r, n):
    raise NotImplementedError()

@pipeable
def RDropBack(r, n):
    raise NotImplementedError()

@pipeable
def Find(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

@pipeable
def Put(r, x):
    return r.put(x)

@pipeable
def Front(r):
    return r.front

@pipeable
def Back(r):
    return r.back

@pipeable
def Length(r):
    return r.length

@pipeable
def Empty(r):
    return r.empty

@pipeable
def PopFront(r):
    r.popFront()
    return r

@pipeable
def PopBack(r):
    r.popBack()
    return r
