import operator
from enum import Enum
from typing import TypedDict, Callable, Any


class StorageError(Exception):
    ...


class NotFoundError(StorageError):
    ...


class AlreadyInUse(StorageError):
    ...


_Operator = Callable[[Any, Any], Any]


class _Operators(TypedDict):
    eq: _Operator
    gt: _Operator
    lt: _Operator
    ge: _Operator
    le: _Operator
    ne: _Operator
    contains: _Operator


OPERATORS = _Operators(
    eq=operator.eq,
    gt=operator.gt,
    lt=operator.lt,
    ge=operator.ge,
    le=operator.le,
    ne=operator.ne,
    contains=lambda c, v: c.in_(v),
)
