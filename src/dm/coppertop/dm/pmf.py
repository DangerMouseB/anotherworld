# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************


import numpy as np
import scipy.stats
from coppertop.bits import pipeable, binary, unary1
from coppertop.std import sort, fvPairs, struct, both, values, fields

from .misc import sequence


@pipeable
def normalise(pmf):
    factor = 1 / sum(pmf >> values)
    answer = struct(pmf)
    for k, v in answer >> fvPairs:
        answer[k] = v * factor
    return answer


@pipeable
def uniform(nOrXs):
    '''Makes a uniform PMF. xs can be sequence of values or [length]'''
    # if a single int it is a count else there must be many xs
    answer = struct()
    if len(nOrXs) == 1:
        if isinstance(nOrXs[0], int):
            n = nOrXs[0]
            p = 1.0 / n
            for x in sequence(0, n-1):
                answer[float(x)] = p
            return answer
    p = 1.0 / len(nOrXs)
    for x in nOrXs:
        answer[float(x)] = p
    return answer


@pipeable(flavour=binary)
def mix(*args):
    """mix(args) where each arg is (beta, pmf) or pmf (beta is assumed to be 1.0)"""
    t = {}
    for arg in args:
        beta, pmf = arg if isinstance(arg, tuple) else (1.0, arg)
        for x, p in pmf >> fvPairs:
            t[x] = t.setdefault(x, 0) + beta * p
    return t >> sort >> normalise


@pipeable(flavour=unary1)
def mean(pmf):
    return np.average(list(pmf >> fields), weights=list(pmf >> values))
    # if pmf:
    #     answer = 0
    #     for x, p in pmf >> fvPairs:
    #         answer += x * p
    #     return answer
    # else:
    #     return np.nan


@pipeable
def kde(xs, data):
    pdf = scipy.stats.gaussian_kde(data)
    answer = {}
    answer._kde = pdf
    for x in xs:
        answer[x] = pdf.evaluate(x)[0]
    return answer >> normalise


# # before
# @pipeable
# def PMul(lhs, rhs):
#     if not isinstance(lhs, (PMF, Likelihood)): raise TypeError('lhs must be a PMF or Likelihood')
#     if not isinstance(rhs, (PMF, Likelihood)): raise TypeError('rhs must be a PMF or Likelihood')
#     if isinstance(lhs, Likelihood) and isinstance(rhs, Likelihood) : raise TypeError("can't both be Likelihoods")
#     xs, ps, kwargs = [], [], {}
#     xs1, ps1, kws1 = lhs._xspskwargs()
#     xs2,  ps2, kws2 = rhs._xspskwargs()
#     assert (xs1 >> Len) == (xs2 >> Len)
#     for (x1, p1, x2, p2) in zip(xspsLHS[0], xspsLHS[1], xspsRHS[0], xspsRHS[1]):
#         if isinstance(p1, (int, float)):
#
#         if x1 != x2: raise TypeError('%s != %s' % (x1, x2))
#         xs.append(x1)
#         ps.append(p1 * p2)
#     return PMF(xs, _normalised(ps), **kwargs)

# after
@pipeable(flavour=binary)
def pmfMul(lhs, rhs):
    # pmf(lhs kvs '{(x.k, x.v*(y.v)} (rhs kvs)) normalise
    return struct(both(
        lhs >> fvPairs,
        lambda fv1, fv2: (fv1[0], fv1[1] * fv2[1]),
        rhs >> fvPairs
    )) >> normalise
