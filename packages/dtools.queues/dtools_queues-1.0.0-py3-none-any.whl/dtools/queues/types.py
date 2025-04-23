# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
### Queue based data structures with restrictive API's

- stateful queue data structures with amortized O(1) pushes and pops each end
- obtaining length (number of elements) of a queue is an O(1) operation
- implemented in a "has-a" relationship with a Python list based circular array
- these data structures will resize themselves larger as needed

#### Queue types

- *class* FIFOQueue: First-In-First-Out Queue
- *class* LIFOQueue: Last-In-First-Out Queue
- *class* DoubleQueue: Double-Ended Queue

"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Never, overload, TypeVar
from dtools.circular_array.ca import CA
from dtools.fp.err_handling import MB

__all__ = [
    'DoubleQueue',
    'FIFOQueue',
    'LIFOQueue',
    'double_queue',
    'fifo_queue',
    'lifo_queue'
]

D = TypeVar('D')  # Needed only for pdoc documentation generation. Makes
L = TypeVar('L')  # linters unhappy when used on function and method signatures
R = TypeVar('R')  # due to "redefined-outer-name" warnings. Function/method 
U = TypeVar('U')  # signatures do not support variance and bounds constraints.


class FIFOQueue[D]:
    """FIFO Queue

    - stateful First-In-First-Out (FIFO) data structure
    - initial data pushed on in natural FIFO order

    """

    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        if (size := len(dss)) < 2:
            self._ca = CA(dss[0]) if size == 1 else CA()
        else:
            msg = f'FIFOQueue expects at most 1 iterable argument, got {size}'
            raise ValueError(msg)

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, FIFOQueue):
            return False
        return self._ca == other._ca

    @overload
    def __getitem__(self, idx: int, /) -> D: ...
    @overload
    def __getitem__(self, idx: slice, /) -> Sequence[D]: ...

    def __getitem__(self, idx: int | slice, /) -> D | Sequence[D] | Never:
        if isinstance(idx, slice):
            msg = 'dtool.restictive queues are not slicable by design'
            raise NotImplementedError(msg)
        return self._ca[idx]

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'FQ()'
        return 'FQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '<< ' + ' < '.join(map(str, self)) + ' <<'

    def copy(self) -> FIFOQueue[D]:
        """Return a shallow copy of the `FIFOQueue`."""
        return FIFOQueue(self._ca)

    def push(self, *ds: D) -> None:
        """Push data onto `FIFOQueue`, does not return a value."""
        self._ca.pushr(*ds)

    def pop(self) -> MB[D]:
        """Pop data from `FIFOQueue`.

        - pop item off queue, return item in a maybe monad
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popl())
        return MB()

    def peak_last_in(self) -> MB[D]:
        """Peak last data into `FIFOQueue`.

        - return a maybe monad of the last item pushed to queue
        - does not consume the data
        - if item already popped, return `MB()`

        """
        if self._ca:
            return MB(self._ca[-1])
        return MB()

    def peak_next_out(self) -> MB[D]:
        """Peak next data out of `FIFOQueue`.

        - returns a maybe monad of the next item to be popped from the queue.
        - does not consume it the item
        - returns `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[0])
        return MB()

    def fold[L](self, f: Callable[[L, D], L], initial: L | None = None, /) -> MB[L]:
        """Reduce with `f` with an optional initial value.

        - folds in natural FIFO Order (oldest to newest)
        - note that when an initial value is not given then `~L = ~D`
        - if iterable empty & no initial value given, return `MB()`
        - traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldl(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> FIFOQueue[U]:
        """Map over the `FIFOQueue`.

        - map function `f` over the queue
          - oldest to newest
          - retain original order
        - returns a new instance

        """
        return FIFOQueue(map(f, self._ca))


class LIFOQueue[D]:
    """LIFO Queue.

    - stateful Last-In-First-Out (LIFO) data structure
    - initial data pushed on in natural LIFO order

    """

    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        if (size := len(dss)) < 2:
            self._ca = CA(dss[0]) if size == 1 else CA()
        else:
            msg = f'LIFOQueue expects at most 1 iterable argument, got {size}'
            raise TypeError(msg)

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, LIFOQueue):
            return False
        return self._ca == other._ca

    @overload
    def __getitem__(self, idx: int, /) -> D: ...
    @overload
    def __getitem__(self, idx: slice, /) -> Sequence[D]: ...

    def __getitem__(self, idx: int | slice, /) -> D | Sequence[D] | Never:
        if isinstance(idx, slice):
            msg = 'dtool.restictive queues are not slicable by design'
            raise NotImplementedError(msg)
        return self._ca[idx]

    def __iter__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'LQ()'
        return 'LQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '|| ' + ' > '.join(map(str, self)) + ' ><'

    def copy(self) -> LIFOQueue[D]:
        """Return a shallow copy of the `LIFOQueue`."""
        return LIFOQueue(reversed(self._ca))

    def push(self, *ds: D) -> None:
        """Push data onto `LIFOQueue`, does not return a value."""
        self._ca.pushr(*ds)

    def pop(self) -> MB[D]:
        """Pop data from `LIFOQueue`.

        - pop item off of queue, return item in a maybe monad
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popr())
        return MB()

    def peak(self) -> MB[D]:
        """Peak next data out of `LIFOQueue`.

        - return a maybe monad of the next item to be popped from the queue
        - does not consume the item
        - returns `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[-1])
        return MB()

    def fold[R](self, f: Callable[[D, R], R], initial: R | None = None, /) -> MB[R]:
        """Reduce with `f` with an optional initial value.

        - folds in natural LIFO Order (newest to oldest)
        - note that when an initial value is not given then `~R = ~D`
        - if iterable empty & no initial value given, return `MB()`
        - traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldr(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> LIFOQueue[U]:
        """Map Over the `LIFOQueue`.

        - map the function `f` over the queue
          - newest to oldest
          - retain original order
        - returns a new instance

        """
        return LIFOQueue(reversed(CA(map(f, reversed(self._ca)))))


class DoubleQueue[D]:
    """Double Ended Queue

    - stateful Double-Ended (DEQueue) data structure
    - order of initial data retained

    """

    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        if (size := len(dss)) < 2:
            self._ca = CA(dss[0]) if size == 1 else CA()
        else:
            msg = f'DoubleQueue expects at most 1 iterable argument, got {size}'
            raise TypeError(msg)

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, DoubleQueue):
            return False
        return self._ca == other._ca

    @overload
    def __getitem__(self, idx: int, /) -> D: ...
    @overload
    def __getitem__(self, idx: slice, /) -> Sequence[D]: ...

    def __getitem__(self, idx: int | slice, /) -> D | Sequence[D] | Never:
        if isinstance(idx, slice):
            msg = 'dtool.restictive queues are not slicable by design'
            raise NotImplementedError(msg)
        return self._ca[idx]

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'DQ()'
        return 'DQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '>< ' + ' | '.join(map(str, self)) + ' ><'

    def copy(self) -> DoubleQueue[D]:
        """Return a shallow copy of the `DoubleQueue`."""
        return DoubleQueue(self._ca)

    def pushl(self, *ds: D) -> None:
        """Push data onto left side (front) of `DoubleQueue`.

        - does not return a value

        """
        self._ca.pushl(*ds)

    def pushr(self, *ds: D) -> None:
        """Push data onto right side (rear) of `DoubleQueue`.

        - like a Python List, does not return a value

        """
        self._ca.pushr(*ds)

    def popl(self) -> MB[D]:
        """Pop Data from left side (front) of `DoubleQueue`.

        - pop left most item off of queue, return item in a maybe monad
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popl())
        return MB()

    def popr(self) -> MB[D]:
        """Pop Data from right side (rear) of `DoubleQueue`.

        - pop right most item off of queue, return item in a maybe monad
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popr())
        return MB()

    def peakl(self) -> MB[D]:
        """Peak left side of `DoubleQueue`.

        - return left most value in a maybe monad
        - does not consume the item
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[0])
        return MB()

    def peakr(self) -> MB[D]:
        """Peak right side of `DoubleQueue`.

        - return right most value in a maybe monad
        - does not consume the item
        - returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[-1])
        return MB()

    def foldl[L](self, f: Callable[[L, D], L], initial: L | None = None, /) -> MB[L]:
        """Reduce left to right with `f` using an optional initial value.

        - note that when an initial value is not given then `~L = ~D`
        - if iterable empty & no initial value given, return `MB()`
        - traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldl(f, initial=initial))

    def foldr[R](self, f: Callable[[D, R], R], initial: R | None = None, /) -> MB[R]:
        """Reduce right to left with `f` using an optional initial value.

        - note that when an initial value is not given then `~R = ~D`
        - if iterable empty & no initial value given, return `MB()`
        - traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldr(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> DoubleQueue[U]:
        """`Map a function over `DoubleQueue`.

        - map the function `f` over the `DoubleQueue`
          - left to right
          - retain original order
        - returns a new instance

        """
        return DoubleQueue(map(f, self._ca))


def fifo_queue[D](*ds: D) -> FIFOQueue[D]:
    """Create a FIFOQueue from the arguments."""
    return FIFOQueue(ds)


def lifo_queue[D](*ds: D) -> LIFOQueue[D]:
    """Create a LIFOQueue from the arguments."""
    return LIFOQueue(ds)


def double_queue[D](*ds: D) -> DoubleQueue[D]:
    """Create a DoubleQueue from the arguments."""
    return DoubleQueue(ds)
