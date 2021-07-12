# *******************************************************************************
#
#    Copyright (c) 2019-2021 David Briant. All rights reserved.
#
# *******************************************************************************


# A python implementation of  https://wiki.dlang.org/Component_programming_with_ranges


from coppertop.bits import pipeable, Null, unary1
from src.time.coppertop.time import addPeriod, DaySecond, AbstractDate
from coppertop.ranges._ranges import ChunkUsingSubRangeGeneratorFR, FnAdapterFR, ChunkFROnChangeOf, IForwardRange, \
    EMPTY, toIndexableFR
from coppertop.std import day, weekday, weekdayName, materialise, rEach, count, monthLongName, _, rjust, cjust, \
    toStr, join, wrapInList, replaceWith, rChain, rUntil


@pipeable
def datesInYear(year):
     return FnAdapterFR(_ithDateInYear(year, _))
@pipeable
def _ithDateInYear(year, i):
    ithDate = AbstractDate(year, 1, 1) >> addPeriod(_, DaySecond(i))
    return EMPTY if ithDate.year != year else ithDate


@pipeable
def monthChunks(datesR):
    return ChunkFROnChangeOf(datesR, lambda x: x.month)


@pipeable
def _untilWeekdayName(datesR, wdayName):
    return datesR >> rUntil >> (lambda d: d >> weekday >> weekdayName == wdayName)
@pipeable
def weekChunks(r):
    return ChunkUsingSubRangeGeneratorFR(r, _untilWeekdayName(_, wdayName='Sun'))


@pipeable
def dateAsDayString(d):
    return d >> day >> toStr >> rjust(_, 3)


@pipeable
class WeekStringsRange(IForwardRange):
    def __init__(self, rOfWeeks):
        self.rOfWeeks = rOfWeeks

    @property
    def empty(self):
        return self.rOfWeeks.empty

    @property
    def front(self):
        # this exhausts the front week range
        week = self.rOfWeeks.front
        startDay = week.front >> weekday
        preBlanks = ['   '] * startDay
        dayStrings = week >> rEach >> dateAsDayString >> materialise
        postBlanks = ['   '] * (7 - ((dayStrings >> count) + startDay))
        return (preBlanks + dayStrings + postBlanks) >> join >> ''

    def popFront(self):
        self.rOfWeeks.popFront()

    def save(self):
        # TODO delete once we've debugged the underlying save issue
        return WeekStringsRange(self.rOfWeeks.save())
weekStrings = unary1('weekStrings', unary1, WeekStringsRange)


@pipeable
def monthTitle(month, width):
    return month >> monthLongName >> cjust(_, width)


@pipeable
def monthLines(monthDays):
    return [
        monthDays.front.month >> monthTitle(_, 21) >> wrapInList >> toIndexableFR,
        monthDays >> weekChunks >> weekStrings
    ] >> rChain


@pipeable
def monthStringsToCalendarRow(strings, blank, sep):
    return strings >> materialise >> replaceWith(Null, blank) >> join(_, sep)


def pasteBlocks(rOfMonthChunk):
    return rOfMonthChunk >> RaggedZipIR >> rEach >> monthStringsToCalendarRow(" "*21, " ")

