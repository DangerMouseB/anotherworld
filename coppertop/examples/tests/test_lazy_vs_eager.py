# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

from coppertop import pipeable, binary2
from coppertop.std import each
from coppertop.ranges import FnAdapterFR, EMPTY, FnAdapterEager
from coppertop.examples.format_calendar import DaySecond
from coppertop.time import addPeriod, parseAbstractDate, YYYY_MM_DD

from coppertop.std import day, assertEquals, rEach, materialise, _


@pipeable
def _ithDateBetween(start, end, i):
    ithDate = start >> addPeriod(_, DaySecond(i))
    return EMPTY if ithDate > end else ithDate

@pipeable(flavour=binary2)
def datesBetween(start, end):
     return FnAdapterFR(_ithDateBetween(start, end, _))

@pipeable(flavour=binary2)
def datesBetweenEager(start, end):
     return FnAdapterEager(_ithDateBetween(start, end, _))


def test_datesBetween_lazy():
    ('2020.01.16' >> parseAbstractDate(_, YYYY_MM_DD)) >> datesBetween >> ('2020.01.29' >> parseAbstractDate(_, YYYY_MM_DD)) \
    >> rEach >> day \
    >> materialise >> assertEquals >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

def test_datesBetween_eager():
    ('2020.01.16' >> parseAbstractDate(_, YYYY_MM_DD)) >> datesBetweenEager >> ('2020.01.29' >> parseAbstractDate(_, YYYY_MM_DD)) \
    >> each >> day \
    >> assertEquals >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

def main():
    test_datesBetween_lazy()
    test_datesBetween_eager()

if __name__ == '__main__':
    main()
    print('pass')

