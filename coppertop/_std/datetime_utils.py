# *******************************************************************************
#
#    Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# *******************************************************************************


# TODO handle locales


import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)


from .._pipe import pipeable
from .._core import Missing


@pipeable
def Year(x):
    return x.year

@pipeable
def Month(x):
    return x.month

@pipeable
def Day(x):
    return x.day

@pipeable
def Hour(x):
    return x.hour

@pipeable
def Minute(x):
    return x.minute

@pipeable
def Second(x):
    return x.second

@pipeable
def Weekday(x):
    return x.weekday()

@pipeable
def WeekdayName(x, locale=Missing):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x]

@pipeable
def WeekdayLongName(x, locale=Missing):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]

@pipeable
def MonthName(month, locale=Missing):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1]

@pipeable
def MonthLongName(month, locale=Missing):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month - 1]


