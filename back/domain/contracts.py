from typing import TypeAlias, TypedDict
from enum import Enum


IdentifierType: TypeAlias = int
Token: TypeAlias = str


class UserRole(Enum):
    manager = 'manager'
    employee = 'employee'


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


class States(Enum):
    good = Good
    average = Average
    bad = Bad


class FactorType(Enum):
    text = 'text'
    single = 'single'


class DayTime(Enum):
    morning = 'morning'
    evening = 'evening'


INSTRUCTION = "Здравствуйте, {name}. Делайте хорошо, а плохо не делайте. Досведания <3"


RECOMMENDATIONS = "Дорогой {name}. Рекомендую тебе следовать всем рекомендациям специалистов."
