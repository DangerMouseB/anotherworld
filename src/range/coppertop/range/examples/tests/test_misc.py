# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************



from ..misc import Fred
from coppertop.std import assertEquals, toStr, cout

def test_repr_or_str():
    [Fred(1)] >> toStr >> assertEquals >> '[rep(1)]'


def main():
    test_repr_or_str()


if __name__ == '__main__':
    main()
    cout << 'pass\n'

