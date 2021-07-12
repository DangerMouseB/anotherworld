# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


from coppertop.std import assertEquals
from ..count_lines_jsp import countLinesJsp, countLinesTrad, countLinesRanges1, countLinesRanges2, countLinesRanges3


home = '/Users/david/repos/github/DangerMouseB/coppertop/coppertop/examples/tests/'
filename = "linesForCounting.txt"
expected = [
    ('aaa\n', 2),
    ('bb\n', 1),
    ('aaa\n', 1),
    ('bb\n', 3),
    ('aaa\n', 1)
]

def main():
    with open(home + filename) as f:
        actual = countLinesJsp(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesTrad(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges1(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges2(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges3(f)
    actual >> assertEquals >> expected


if __name__ == '__main__':
    main()
    print('pass')

