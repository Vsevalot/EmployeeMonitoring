from fastapi import APIRouter, Depends

from services.state import StateService
from ports.api.v1.dependencies import get_state_service

from ports.api.v1.schemas import StatesResponse, State


router = APIRouter(tags=["States"])


@router.get("/v1/states")
async def get_states(
    state_service: StateService = Depends(get_state_service),
) -> StatesResponse:
    states = await state_service.get_list()
    return StatesResponse(
        res=[State(id=s["id"], value=s["value"], name=s["name"]) for s in states]
    )
