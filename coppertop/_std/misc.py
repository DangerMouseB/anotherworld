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
import builtins


# conversions

@pipeable
def ToStr(x):
    return str(x)

@pipeable
def ToInt(a):
    return int(a)

@pipeable
def ToRepr(x):
    return str(x)

@pipeable
def ToString(format, x):
    raise NotImplementedError('ToString')


# other

@pipeable
def Not(x):
    return not x

@pipeable
def getAttr(x, name):
    return getattr(x, name)

@pipeable
def max(iter):
    return builtins.max(iter)

@pipeable
def min(iter):
    return builtins.min(iter)



