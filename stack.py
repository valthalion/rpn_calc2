from typing import Any, Iterable, List, Optional, Tuple, Union

from errors import NotEnoughArgumentsError


class Stack:
    def __init__(self) -> None:
        self._stack: List = []

    def __bool__(self) -> bool:
        return len(self._stack) > 0

    def __len__(self) -> int:
        return len(self._stack)

    def __iter__(self) -> Iterable:
        return iter(self._stack)

    def __getitem__(self, key: int) -> float:
        return self._stack[key]

    def push(self, value: Any) -> None:
        self._stack.append(value)

    def push_iter(self, v):
        self._stack.extend(v)

    def pop(self, n: int = 1) -> Union[Tuple, Any]:
        if len(self._stack) < n:
            raise NotEnoughArgumentsError('Too few arguments')
        if n == 1:
            return self._stack.pop()
        self._stack, result = self._stack[:-n], self._stack[-n:]
        return tuple(result)

    def pop_iter(self, n: int = 1) -> Union[Tuple, Any]:
        if len(self._stack) < n:
            raise NotEnoughArgumentsError('Too few arguments')
        self._stack, result = self._stack[:-n], self._stack[-n:]
        return tuple(result)

    def peek(self, n: int = 1) -> Union[Tuple, Any]:
        if len(self._stack) < n:
            raise NotEnoughArgumentsError('Too few arguments')
        if n == 1:
            return self._stack[-1]
        return tuple(self._stack[-n:])

    def clear(self) -> None:
        self._stack = []
