from typing import Annotated

from ports.api.v1.schemas import ParticipantListResponse, Participant, ParticipantSingleResponse

from fastapi import APIRouter, Depends
from domain.entities import User
from ports.api.v1.dependencies import (
    get_current_user,
)


router = APIRouter(tags=["Participants"])


@router.get("/v1/participants")
async def get_participants(
    user: User = Depends(get_current_user),
) -> ParticipantListResponse:
    return ParticipantListResponse(result=[])


@router.get("/v1/participants/me")
async def get_me(
        user: User = Depends(get_current_user),
) -> ParticipantSingleResponse:
    return ParticipantSingleResponse(result=Participant(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        surname=user['surname'],
        phone=user['phone'],
        company=user['business_unit']['company']['name'],
        position=user['position'],
        email=user['email'],
        birthdate=user['birthdate'],
    ))
