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
# from ..ranges import RMap


@pipeable
def sort(x, key=None, reverse=False):
    if isinstance(x, dict):
        return dict(sorted(x.items(), key=key, reverse=reverse))
    else:
        return sorted(x, key=key, reverse=reverse)


@pipeable
def count(iter):
    return len(iter)

@pipeable
def WrapInList(x):
    l = []
    l.append(x)
    return l

@pipeable
def First(x):
    raise NotImplementedError()

@pipeable
def Last(x):
    raise NotImplementedError()

@pipeable
def Take(x):
    raise NotImplementedError()

@pipeable
def Cut(x):
    raise NotImplementedError()

@pipeable
def ReplaceWith(haystack, needle, replacement):
    return haystack >> RMap >> (lambda e: replacement if e == needle else e)


