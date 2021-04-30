# *******************************************************************************
#
#    Copyright (c) 2019-2020 David Briant. All rights reserved.
#
# *******************************************************************************


from __future__ import annotations

from coppertop import pipeable
from typing import Any, Union
import sys


# empty - checks for end-of-input and fills a one-element buffer held inside the range object
# front - returns the buffer
# popFront() - sets an internal flag that tells empty to read the next element when called
# moveFront() - moves to the start

class IInputRange(object):
    @property
    def empty(self) -> bool:
        raise NotImplementedError()
    @property
    def front(self) -> Any:
        raise NotImplementedError()
    def popFront(self) -> None:
        raise NotImplementedError()
    def moveFront(self) -> Any:
        raise NotImplementedError()

    # assignable
    @front.setter
    def front(self, value: Any) -> None:
        raise NotImplementedError()

    # python iterator interface
    # this is convenient but possibly too convenient and it may muddy things hence the ugly name
    @property
    def _GetIRIter(self):
        return IInputRange._Iter(self)

    class _Iter(object):
        def __init__(self, r):
            self.r = r
        def __iter__(self) -> IInputRange:
            return self
        def __next__(self) -> Any:
            if self.r.empty: raise StopIteration
            answer = self.r.front
            self.r.popFront()
            return answer

@pipeable(leftToRight=True, pipeOnly=True)
def GetIRIter(r):
    # the name is deliberately semi-ugly to discourge but not prevent
    return r._GetIRIter


class IForwardRange(IInputRange):
    def save(self) -> IForwardRange:
        raise NotImplementedError()


class IBidirectionalRange(IForwardRange):
    @property
    def back(self) -> Any:
        raise NotImplementedError()
    def moveBack(self) -> Any:
        raise NotImplementedError()
    def popBack(self) -> None:
        raise NotImplementedError()

    # assignable
    @back.setter
    def back(self, value: Any) -> None:
        raise NotImplementedError()


class IRandomAccessFinite(IBidirectionalRange):
    def moveAt(self, i: int) -> Any:
        raise NotImplementedError()
    def __getitem__(self, i: Union[int, slice]) -> Union[Any, IRandomAccessFinite]:
        raise NotImplementedError()
    @property
    def length(self) -> int:
        raise NotImplementedError()

    # assignable
    def __setitem__(self, i: int, value: Any) -> None:
        raise NotImplementedError()


class IRandomAccessInfinite(IForwardRange):
    def moveAt(self, i: int) -> Any:
        raise NotImplementedError()

    def __getitem__(self, i: int) -> Any:
        """Answers an element"""
        raise NotImplementedError()


class IOutputRange(object):
    def put(self, value: Any):
        """Answers void"""
        raise NotImplementedError()
