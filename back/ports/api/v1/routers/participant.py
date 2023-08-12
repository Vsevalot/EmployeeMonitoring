from typing import Annotated

from fastapi import APIRouter, Header

from ports.api.v1.schemas import ParticipantResponse


router = APIRouter(tags=["Participants"])


@router.get("/v1/participants")
async def get_participants(
    authorization: Annotated[str | None, Header()],
) -> ParticipantResponse:
    return ParticipantResponse(result=[])
