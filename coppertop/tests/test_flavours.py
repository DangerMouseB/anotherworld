# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************

from coppertop import assertRaises
from bones_pipe.std import assertEquals
from coppertop import pipeable, nullary, rau, binary, ternary


def prettyArgs(*args):
    return ', '.join([str(arg) for arg in args])


@pipeable(flavour=nullary)
def nullary0():
    return 'nullary0'

@pipeable(flavour=nullary)
def nullary1(a):
    return f'nullary1({prettyArgs(a)})'

@pipeable(flavour=nullary)
def nullary2(a, b):
    return f'nullary2({prettyArgs(a, b)})'

@pipeable
def unary1(a):
    return f'unary1({prettyArgs(a)})'

@pipeable
def unary2(a, b):
    return f'unary2({prettyArgs(a, b)})'

@pipeable
def unary3(a, b, c):
    return f'unary3({prettyArgs(a, b, c)})'

@pipeable(flavour=rau)
def rau1(a):
    return f'rau1({prettyArgs(a)})'

@pipeable(flavour=rau)
def rau2(a, b):
    return f'rau2({prettyArgs(a, b)})'

@pipeable(flavour=rau)
def rau3(a, b, c):
    return f'rau3({prettyArgs(a, b, c)})'

@pipeable(flavour=binary)
def binary2(a, b):
    return f'binary2({prettyArgs(a, b)})'

@pipeable(flavour=binary)
def binary3(a, b, c):
    return f'binary3({prettyArgs(a, b, c)})'

@pipeable(flavour=ternary)
def ternary3(a, b, c):
    return f'ternary3({prettyArgs(a, b, c)})'



def testNullary():
    str(nullary1(1)) >> assertEquals >> 'nullary1(1)'
    str(nullary2(1, ...)) >> assertEquals >> 'nullary2(1, ...)'
    str(nullary2(1, ...)(2)) >> assertEquals >> 'nullary2(1, 2)'

    with assertRaises(SyntaxError) as e:
        nullary1(...)(1, 2)
    e.exceptionValue.args[0] >> assertEquals >> 'too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        2 >> nullary2(1, ...)
    e.exceptionValue.args[0] >> assertEquals >> 'syntax not of form nullary()'


def testUnary():
    str(unary1(1)) >> assertEquals >> 'unary1(1)'
    str(unary2(1, ...)) >> assertEquals >> 'unary2(1, ...)'
    str(2 >> unary2(1, ...)) >> assertEquals >> 'unary2(1, 2)'

    with assertRaises(SyntaxError) as e:
        unary1(...)(1, 2)
    e.exceptionValue.args[0] >> assertEquals >> 'too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        2 >> unary3(1, ..., ...)
    e.exceptionValue.args[0] >> assertEquals >> 'needs 2 args but 1 will be piped'

    str(nullary1(1) >> unary1) >> assertEquals >> 'unary1(nullary1(1))'


def testRau():
    str(rau1(1)) >> assertEquals >> 'rau1(1)'
    str(rau2(1, ...)) >> assertEquals >> 'rau2(1, ...)'
    str(rau2(1, ...) >> 2) >> assertEquals >> 'rau2(1, 2)'

    with assertRaises(SyntaxError) as e:
        rau1(...)(1, 2)
    e.exceptionValue.args[0] >> assertEquals >> 'too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        rau3(1, ..., ...) >> 2
    e.exceptionValue.args[0] >> assertEquals >> 'needs 2 args but 1 will be piped'

    str(rau1 >> 1) >> assertEquals >> 'rau1(1)'
    str(rau1 >> nullary1(1)) >> assertEquals >> 'rau1(nullary1(1))'

    with assertRaises(TypeError) as e:
        rau1 >> unary1
    with assertRaises(TypeError) as e:
        rau1 >> binary2
    with assertRaises(TypeError) as e:
        rau1 >> ternary3



def testBinary():
    # in python we can't stop partial binding of binaries as we don't have access to the parser
    str(binary2(1, 2)) >> assertEquals >> 'binary2(1, 2)'
    str(1 >> binary3(..., 2, ...)) >> assertEquals >> 'binary3(1, 2, ...)'
    str(1 >> binary3(..., 2, ...) >> 3) >> assertEquals >> 'binary3(1, 2, 3)'
    str(1 >> binary2 >> 2) >> assertEquals >> 'binary2(1, 2)'
    str(1 >> binary2 >> unary1) >> assertEquals >> 'binary2(1, unary1)'



def testTernary():
    # consider the following - it shows that rau, binary, ternary overwrite any function as args r1 or r2
    str([1, 2] >> ternary3 >> binary2 >> [3, 4]) >> assertEquals >> 'ternary3([1, 2], binary2, [3, 4])'
    str([1, 2] >> ternary3 >> binary3(..., 2, ...) >> [3, 4]) >> assertEquals >> 'ternary3([1, 2], binary3(..., 2, ...), [3, 4])'



# def testExamples():
#     join = MultiFunction('join', Binary)
#     mul = MultiFunction('mul', Binary)
#     add = MultiFunction('add', Binary)
#     fred = MultiFunction('fred', Unary)
#     eachBoth = MultiFunction('eachBoth', Ternary)
#     each = MultiFunction('each', Binary)
#     inject = MultiFunction('inject', Binary)
#
#     str([1, 2] >> each >> fred) >> assertEquals >> 'each([1, 2], fred)'
#     str([1, 2] >> join >> mul >> fred) >> assertEquals >> 'fred(join([1, 2], mul))'
#     str([1, 2] >> inject(..., 0, ...) >> add) >> assertEquals >> 'inject([1, 2], 0, add)'
#     str([1, 2] >> eachBoth >> mul >> [2, 4] >> fred) >> assertEquals >> 'fred(eachBoth([1, 2], mul, [2, 4]))'
#
#     with assertRaises(SyntaxError) as e:
#         [1, 2] >> each(..., fred)
#     e.exceptionValue.args[0] >> assertEquals >> 'needs 1 args but 2 will be piped'



def main():
    testNullary()
    testUnary()
    testRau()
    testBinary()
    testTernary()
    # testExamples()


if __name__ == '__main__':
    main()
    print('pass')


