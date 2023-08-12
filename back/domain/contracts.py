from typing import TypeAlias
from enum import Enum


IdentifierType: TypeAlias = int


class UserType(Enum):
    admin = 0
    manager = 1
    employee = 2
