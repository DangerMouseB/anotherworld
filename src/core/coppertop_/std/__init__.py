# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
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
from .wip import *

from ._core import _

if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__ + ' - done')
