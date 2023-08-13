from typing import TypeAlias
from enum import Enum


IdentifierType: TypeAlias = int


class UserType(Enum):
    admin = 0
    manager = 1
    employee = 2


Bad = {
    "id": 1,
    "name": "Плохо",
    "value": 100,
}

Average = {
    "id": 2,
    "name": "Средне",
    "value": 200,
}

Good = {
    "id": 3,
    "name": "Хорошо",
    "value": 300,
}


class Mood(Enum):
    good = Good
    average = Average
    bad = Bad
