from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel, field_validator
import datetime

from config import DAYS_FOR_GROUP_STAT
from domain.contracts import IdentifierType, DayTime
from domain.entities import User, Feedback


GOOD_VALUE = 300


class MorningBody(BaseModel):
    state_id: IdentifierType


class EveningBody(BaseModel):
    state_id: IdentifierType
    factor_id: IdentifierType | None = None


class State(BaseModel):
    id: IdentifierType
    name: str
    value: int


class FeedbackResponse(BaseModel):
    morning: State | None = None
    evening: State | None = None

    @classmethod
    def from_feedbacks(cls, morning: Feedback | None, evening: Feedback | None):
        if morning:
            morning = State(
                id=morning["state"].id,
                name=morning["state"].name,
                value=morning["state"].value,
            )
        if evening:
            evening = State(
                id=evening["state"].id,
                name=evening["state"].name,
                value=evening["state"].value,
            )
        return cls(
            morning=morning,
            evening=evening,
        )


class Factor(BaseModel):
    id: IdentifierType
    name: str


class Category(BaseModel):
    id: IdentifierType
    name: str
    factors: list[Factor]


class FactorsResponse(BaseModel):
    result: list[Category]


class InstructionResponse(BaseModel):
    result: str


class StatesResponse(BaseModel):
    result: list[State]


class RegisterBodyBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    birthdate: datetime.date
    phone: str
    position: str
    email: str
    password: str
    personal_data_confirmed: bool

    @field_validator("personal_data_confirmed")
    @classmethod
    def personal_data_confirmed_validator(cls, v: bool) -> bool:
        if not v:
            raise ValueError("personal_data_confirmed must be set to true")
        return v


class ManagerRegisterBody(RegisterBodyBase):
    company: str
    department: str


class ParticipantRegisterBody(RegisterBodyBase):
    manager_id: IdentifierType


class LoginBody(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    result: str


class Participant(BaseModel):
    id: IdentifierType
    first_name: str | None
    last_name: str | None
    surname: str | None
    birthdate: datetime.date | None
    company: str | None
    position: str | None
    phone: str | None
    email: str

    code: str | None

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            surname=user["surname"],
            phone=user["phone"],
            company=user["business_unit"]["company"]["name"],
            position=user["position"],
            email=user["email"],
            birthdate=user["birthdate"],
            code=user["code"],
        )


class ParticipantListResponse(BaseModel):
    result: list[Participant]


class ParticipantSingleResponse(BaseModel):
    result: Participant


class ManagerItem(BaseModel):
    id: IdentifierType
    first_name: str
    last_name: str
    surname: str
    department: str
    company: str


class ManagerResponse(BaseModel):
    result: ManagerItem


class RegistrationResponse(BaseModel):
    result: str


class RecommendationsResponse(BaseModel):
    result: str


class GroupFactor(BaseModel):
    id: IdentifierType
    name: str
    voted: int
    recommendation: str


class GroupStatItem(BaseModel):
    category: str
    factors: list[GroupFactor]


class Happiness(BaseModel):
    percent: int
    recommendation: str


class GroupStatResponse(BaseModel):
    result: list[GroupStatItem]
    happiness: Happiness | None

    @classmethod
    def from_feedbacks(cls, feedbacks: Sequence[Feedback]) -> "GroupStatResponse":
        res = defaultdict(lambda: defaultdict(lambda: dict()))
        first_date = None
        last_date = None
        for f in feedbacks:
            if first_date is None or f['date'] < first_date:
                first_date = f['date']
            if last_date is None or f['date'] > last_date:
                last_date = f['date']
            if not f["factor"]:
                continue
            category = f["factor"]["category"]
            factor_id = f["factor"]["id"]
            recommendation = f["factor"]["manager_recommendation"]
            name = f["factor"]["name"]
            if factor_id not in res[category]:
                res[category][factor_id] = {
                    "recommendation": recommendation,
                    "name": name,
                    "id": factor_id,
                    "voted": 0,
                }
            res[category][factor_id]["voted"] += 1

        result = []
        for category in res:
            factors = []
            for factor_id in res[category]:
                factors.append(GroupFactor(**res[category][factor_id]))
            result.append(GroupStatItem(
                category=category,
                factors=factors,
            ))

        happiness = None
        if first_date and last_date and ((last_date - first_date).days >= DAYS_FOR_GROUP_STAT):
            happiness = cls._get_happiness(feedbacks)
        return cls(result=result, happiness=happiness)

    @classmethod
    def _get_happiness(cls, feedbacks: Sequence[Feedback]) -> Happiness:
        good_feedbacks = [f for f in feedbacks if f['state'].value == GOOD_VALUE]
        percent = int(len(good_feedbacks) * 100 / len(feedbacks))
        recommendation = cls._get_happiness_recommendation(percent)
        return Happiness(percent=percent, recommendation=recommendation)

    @staticmethod
    def _get_happiness_recommendation(percent: int) -> str:
        if percent > 76:
            return "Наличие причин для возникновения конфликтных ситуаций, способных привести к возникновению микрокризиса персонала, выражаемого в форме снижения продуктивности и повышения презентеизма. Ситуация требует дальнейшего наблюдения и тематических бесед с линейным руководителем для обсуждения проблем в трудовом коллективе."
        if percent > 50:
            return "Наличие симптомов кризиса персонала, сигнализирующих о заметном снижении мотивации и продуктивности работников, и повышении уровня презентеизма вследствие эмоциональной нестабильности сотрудников на рабочем месте, обусловленной рядом факторов. Ситуация требует дальнейшего наблюдения и тематических бесед с линейным руководителем, менеджером по персоналу и работниками для обсуждения проблем в трудовом коллективе, проведения опросов персонала, привлечения внешних экспертов для проведения консультаций и поиска управленческих решений, разработки и реализации плана мероприятий по повышению уровня здоровья и благополучия работников, а также снижения уровня презентеизма на рабочем месте."
        if percent > 25:
            return "Наличие кризиса персонала, сопровождаемого значительным снижением мотивации и продуктивности работников, и повышением уровня презентеизма, дестабилизации работы трудового коллектива, обусловленных рядом факторов. Ситуация требует дальнейшего наблюдения, проведения опросов персонала в форме анкетирования и интервьюирования, привлечения внешних экспертов для проведения консультаций и поиска управленческих решений, разработки и внедрения долгосрочной программы «Здоровье и благополучие персонала»."
        return "Наличие ярко выраженного кризиса персонала с полным несоответствием мотивации и результативности работников, а также условий труда требованиям организационных целей и задач. Существует угроза дальнейшей нежизнеспособности существующей системы управления трудовым коллективом. Ситуация требует привлечения внешних экспертов для поиска управленческих и кадровых решений, проведения кадрового аудита, совершенствования стратегии управления человеческими ресурсами и кадровой политики организации."


class ParticipantFactor(BaseModel):
    id: IdentifierType
    name: str
    category: str
    recommendation: str


class ParticipantStatItem(BaseModel):
    date: datetime.date
    morning: State | None = None
    evening: State | None = None
    factor: ParticipantFactor | None = None


class ParticipantStatResponse(BaseModel):
    result: list[ParticipantStatItem]

    @classmethod
    def from_feedback_range(cls, feedback_range: dict[datetime.date, dict[DayTime, Feedback | None]]):
        res = []
        for d, feedbacks in feedback_range.items():
            stat_item = ParticipantStatItem(date=d)

            morning = feedbacks[DayTime.morning]
            if morning:
                stat_item.morning = morning["state"]

            evening = feedbacks[DayTime.evening]
            if evening:
                stat_item.evening = evening["state"]

            if evening and evening["factor"]:
                stat_item.factor = ParticipantFactor(
                    id=evening["factor"]["id"],
                    name=evening["factor"]["name"],
                    category=evening["factor"]["category"],
                    recommendation=evening["factor"]["manager_recommendation"],
                )
            res.append(stat_item)
        return cls(result=res)


class DeviceTokenPayload(BaseModel):
    token: str
