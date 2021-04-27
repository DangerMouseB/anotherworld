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
def Strip(s,  chars=None):
    return s.strip(chars)

@pipeable
def LJust(w, s, pad=" "):
    return s.ljust(w, pad)

@pipeable
def RJust(w, s, pad=" "):
    return s.rjust(w, pad)

@pipeable
def CJust(w, s, pad=" "):
    return s.center(w, pad)

@pipeable
def JoinUsing(strings, sep):
    return sep.join(strings)

@pipeable
def Format(format, thing):
    return format.format(thing)

