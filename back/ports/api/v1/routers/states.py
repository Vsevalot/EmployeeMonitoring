from typing import Annotated

from fastapi import APIRouter, Header

from ports.api.v1.schemas import StatesResponse, State


router = APIRouter(tags=["States"])


@router.get("/v1/states")
async def get_states(
    authorization: Annotated[str | None, Header()],
) -> StatesResponse:
    return StatesResponse(res=[State(id=i, value=f"value {i}") for i in range(1, 4)])
