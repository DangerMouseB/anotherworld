# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************


# SHOULDDO handle locales


import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import datetime
from coppertop.bits import Missing, NotYetImplemented
from coppertop.pipe import pipeable


@pipeable
def year(x):
    return x.year

@pipeable
def month(x):
    return x.month

@pipeable
def day(x):
    return x.day

@pipeable
def hour(x):
    return x.hour

@pipeable
def minute(x):
    return x.minute

@pipeable
def second(x):
    return x.second

@pipeable
def weekday(x):
    return x.weekday()

@pipeable
def weekdayName(x, locale=Missing):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x]

@pipeable
def weekdayLongName(x, locale=Missing):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]

@pipeable
def monthName(month, locale=Missing):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1]

@pipeable
def monthLongName(month, locale=Missing):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month - 1]

@pipeable
def parseDate(s, f):
    if f == 'dd/MM/yyyy':
        return datetime.datetime.strptime(s, '%d/%m/%y').date()
    if f == 'MM/dd/yyyy':
        return datetime.datetime.strptime(s, '%m/%d/%y').date()
    else:
        raise NotYetImplemented()

