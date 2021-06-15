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

from .adverbs import *
from .collections import *
from .datetime import *
from .deprecated import *
from .files import *
from .maths import *
from .misc import *
from .module import *
from .stdio import *
from .string import *
from .struct import *
from .testing import *
from .to_sort import *
from .wip import *

from ._core import _

if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)