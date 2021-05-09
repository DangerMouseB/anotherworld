# *******************************************************************************
#
#    Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# *******************************************************************************



from coppertop import Missing


try:
    import numpy
except:
    numpy = None


def sequence(p1, p2, n=Missing, step=Missing, sigmas=Missing):
    if step is not Missing and n is not Missing:
        raise TypeError('Must only specify either n or step')
    if step is Missing and n is Missing:
        first , last = p1, p2
        return list(range(first, last+1, 1))
    elif n is not Missing and sigmas is not Missing:
        mu, sigma = p1, p2
        low = mu - sigmas * sigma
        high = mu + sigmas * sigma
        return sequence(low, high, n=n)
    elif n is not Missing and sigmas is Missing:
        first , last = p1, p2
        return list(numpy.linspace(first, last, n))
    elif n is Missing and step is not Missing:
        first , last = p1, p2
        return list(numpy.arange(first, last + step, step))
    else:
        raise NotImplementedError('Unhandled case')