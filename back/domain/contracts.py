from typing import TypeAlias, TypedDict
from enum import Enum


IdentifierType: TypeAlias = int
Token: TypeAlias = str


class UserRole(Enum):
    manager = 'manager'
    participant = 'participant'


class FactorType(Enum):
    text = 'text'
    single = 'single'


class DayTime(Enum):
    morning = 'morning'
    evening = 'evening'


INSTRUCTION = "Здравствуйте, {name}. Делайте хорошо, а плохо не делайте. Досведания <3"


RECOMMENDATIONS = "Дорогой {name}. Рекомендую тебе следовать всем рекомендациям специалистов."
