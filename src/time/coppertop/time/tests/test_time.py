# *******************************************************************************
#
#    Copyright (c) 2020 DDavid Briant. All rights reserved.
#
# *******************************************************************************

from coppertop.std import assertEquals
from .._core import AbstractDateTime, AbstractDate, ObservedTimeOfDay, ObservedDateTime, AbstractTimeOfDay, Precision, \
    ParseAbstractDateTime, parseAbstractDate, ParseObservedTimeOfDay, ParseObservedDateTime, ParseObserversCtx, ParseAbstractTimeOfDay, \
    ToString, \
    ObserversCtx, FpMLCity, IanaCity, IanaTz, \
    YYYY_MM_DD
from .._core import _parseDTTz



def test_parsing():
    # Raw
    _parseDTTz("2020.01.01T16:15:00", 'yyyy.MM.ddThh:mm:ss') >> assertEquals >> (2020,1,1,16,15,0,0,Precision.s,None)
    _parseDTTz("2020.01.01T16:15:00 GBLO", 'yyyy.MM.ddThh:mm:ss FFFF') >> assertEquals >> (2020,1,1,16,15,0,0,Precision.s,FpMLCity.GBLO)
    _parseDTTz("2020.01.01 16:15:00.001 Europe/London", 'yyyy.MM.dd hh:mm:ss.ms IIII') >> assertEquals >> (2020,1,1,16,15,0,1000,Precision.ms,IanaCity.Europe_London)
    _parseDTTz("[2020.01.01 16:15:00.0001] BST", '[yyyy.MM.dd hh:mm:ss.us] ZZZZ') >> assertEquals >> (2020,1,1,16,15,0,100,Precision.us,IanaTz.BST)


    # AbstractDateTime
    "2020.01.01 16:15" >> ParseAbstractDateTime(format='yyyy.MM.dd hh:mm') >> assertEquals >> AbstractDateTime(2020, 1, 1, 16, 15)


    # AbstractDate
    "2020.01.01" >> parseAbstractDate(format=YYYY_MM_DD) >> assertEquals >> AbstractDate(2020, 1, 1)


    # ParseDateTimeTz
    "2020.01.01 16:15:0.001 GBLO" >> ParseObservedDateTime(format='yyyy.MM.dd HH:MM:SS.us FFFF') >> assertEquals >> ObservedDateTime(2020, 1, 1, 16, 15, 0, 1, Precision.s)


    # ObservedTimeOfDay


    # AbstractTimeOfDay


    # YMDHMS
    ymdhms = "2020.06.01 16:15:00.0001" >> ParseYMDHMS(format='yyyy.MM.dd HH:MM.us')
    ymdhms >> assertEquals >> YMDHMS(2020,1,1,16,15,0,100,Precision.us)

    ymdhms >> ToTz(FpMLCity.GBLO) >> assertEquals >> ObservedDateTime(
        "2020.06.01" >> parseAbstractDate(format='yyyy.MM.dd'),
        "16:15:00.0001" >> ParseAbstractTimeOfDay(format='HH:MM.SS.us'),
        FpMLCity.GBLO
    )


    # YearMonth
    "H20" >> parseYearMonth(format='HMUZyy') >> assertEquals >> YearMonth(2020,3)
    "H0" >> ParseYearMonth(format='HMUZy', observationDate=AbstractDate(2020, 4, 1)) >> assertEquals >> YearMonth(2030, 3)
    "3/70" >> ParseYearMonth(format='M/yy') >> assertEquals >> YearMonth(1970,3)
    "3/20" >> ParseYearMonth(format='M/yy', century=1900) >> assertEquals >> YearMonth(1920,3)



def test_formatting():
    # u = "2020.01.01 16:15" >> toUTC(kdb)
    AbstractDateTime(2020, 1, 1, 16, 15) >> ToString('yyyy.MM.dd HH:MM AbstractDateTime') >> assertEquals >> 'AbstractDateTime(2020, 1, 1, 16, 15)'
    AbstractDate(2020, 1, 1) >> ToString('') >> assertEquals >> 'AbstractDate(2020, 1, 1)'



def test_tzConversion():
    pass



def main():
    test_parsing()
    test_formatting()
    test_tzConversion()
    print('pass')


if __name__ == '__main__':
    main()


