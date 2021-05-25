# *******************************************************************************
#
#    Copyright (c) 2019-2020 David Briant
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


from coppertop.examples.format_calendar import datesInYear, monthChunks, weekChunks, weekStrings, monthTitle, \
    monthLines, monthStringsToCalendarRow
from coppertop.examples.format_calendar import _untilWeekdayName
from coppertop.time import addPeriod, DaySecond, parseAbstractDate, YYYY_MM_DD, AbstractDate
from coppertop.ranges import EMPTY, getIRIter, ListOR, toIndexableFR, RaggedZipIR, FnAdapterFR, \
    ChunkUsingSubRangeGeneratorFR
from coppertop.std import assertEquals, each, strip, front, take, pushAllTo, not_, _, count, rEach, materialise, \
    day, wrapInList, rChain
from coppertop import Null, PP, pipeable, binary2


# see notes in format_calendar.py


@pipeable
def _ithDateBetween(start, end, i):
    ithDate = start >> addPeriod(_, DaySecond(i))
    return EMPTY if ithDate > end else ithDate

@pipeable(flavour=binary2)
def datesBetween(start, end):
     return FnAdapterFR(_ithDateBetween(start, end, _))



# tests

def main():
    test_allDaysInYear()
    test_datesBetween()
    test_chunkingIntoMonths()
    test_checkNumberOfDaysInEachMonth()
    test__untilWeekdayName()
    test_WeekChunks()
    test_WeekStrings()
    test_MonthTitle()
    test_oneMonthsOutput()
    # test_firstQuarter()
    print('pass')


def test_allDaysInYear():
    actual = []
    o = 2020 >> datesInYear >> pushAllTo >> ListOR(actual)
    actual[0] >> assertEquals >> AbstractDate(2020, 1, 1)
    actual[-1] >> assertEquals >> AbstractDate(2020, 12, 31)
    [e for e in 2020 >> datesInYear >> getIRIter] >> count >> assertEquals >> 366


def test_datesBetween():
    ('2020.01.16' >> parseAbstractDate(_, YYYY_MM_DD)) >> datesBetween >> ('2020.01.29' >> parseAbstractDate(_, YYYY_MM_DD)) \
    >> rEach >> day \
    >> materialise >> assertEquals >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]


def test_chunkingIntoMonths():
    2020 >> datesInYear \
        >> monthChunks \
        >> materialise \
        >> count >> assertEquals >> 12


def test_checkNumberOfDaysInEachMonth():
    2020 >> datesInYear \
        >> monthChunks \
        >> materialise >> each >> count \
        >> assertEquals >> [31,29,31,30,31,30,31,31,30,31,30,31]


def test__untilWeekdayName():
    r = 2020 >> datesInYear
    dates = [d for d in r >> _untilWeekdayName(_, wdayName='Sun') >> getIRIter]
    dates[-1] >> assertEquals >> AbstractDate(2020, 1, 5)   # the sunday
    r >> front >> assertEquals >> AbstractDate(2020, 1, 6) # the monday


def test_WeekChunks():
    datesR = '2020.01.16' >> parseAbstractDate(_, YYYY_MM_DD) >> datesBetween >> ('2020.01.29' >> parseAbstractDate(_, YYYY_MM_DD))
    weeksR = ChunkUsingSubRangeGeneratorFR(datesR, _untilWeekdayName(_, wdayName='Sun'))
    actual = []
    while not weeksR.empty:
        weekR = weeksR >> front
        actual.append([d >> day for d in weekR >> getIRIter])
        weeksR.popFront()
    actual >> assertEquals >> [[16, 17, 18, 19], [20, 21, 22, 23, 24, 25, 26], [27, 28, 29]]


def test_WeekStrings():
    expectedJan2020 = [
        '        1  2  3  4  5',
        '  6  7  8  9 10 11 12',
        ' 13 14 15 16 17 18 19',
        ' 20 21 22 23 24 25 26',
        ' 27 28 29 30 31      ',
    ]
    weekStringsR = (
        2020 >> datesInYear
        >> monthChunks
        >> front
        >> weekChunks
        >> weekStrings
    )
    weekStringsR2 = weekStringsR.save()
    [ws for ws in weekStringsR >> getIRIter] >> assertEquals >> expectedJan2020

    actual = [ws for ws in weekStringsR2 >> getIRIter]
    if actual >> assertEquals(_, _, returnResult=True) >> expectedJan2020 >> not_:
        "fix WeekStringsRange.save()" >> PP


def test_MonthTitle():
    1 >> monthTitle(..., 21) >> wrapInList >> toIndexableFR \
        >> rEach >> strip >> materialise \
        >> assertEquals \
        >> ['January']


def test_oneMonthsOutput():
    [
        1 >> monthTitle(_, width=21) >> wrapInList >> toIndexableFR,
        2020 >> datesInYear
            >> monthChunks
            >> front
            >> weekChunks
            >> weekStrings
    ] >> rChain \
        >> materialise >> assertEquals >> Jan2020TitleAndDateLines

    # equivalently
    assertEquals(
        materialise(monthLines(front(monthChunks(datesInYear(2020))))),
        Jan2020TitleAndDateLines
    )


def test_firstQuarter():
    2020 >> datesInYear \
        >> monthChunks \
        >> take(_, 3) \
        >> RaggedZipIR >> rEach >> monthStringsToCalendarRow(Null, " "*21, " ")



Jan2020DateLines = [
    '        1  2  3  4  5',
    '  6  7  8  9 10 11 12',
    ' 13 14 15 16 17 18 19',
    ' 20 21 22 23 24 25 26',
    ' 27 28 29 30 31      ',
]

Jan2020TitleAndDateLines = ['       January       '] + Jan2020DateLines

Q1_2013TitleAndDateLines = [
    "       January              February                March        ",
    "        1  2  3  4  5                  1  2                  1  2",
    "  6  7  8  9 10 11 12   3  4  5  6  7  8  9   3  4  5  6  7  8  9",
    " 13 14 15 16 17 18 19  10 11 12 13 14 15 16  10 11 12 13 14 15 16",
    " 20 21 22 23 24 25 26  17 18 19 20 21 22 23  17 18 19 20 21 22 23",
    " 27 28 29 30 31        24 25 26 27 28        24 25 26 27 28 29 30",
    "                                             31                  "
]


if __name__ == '__main__':
    main()


