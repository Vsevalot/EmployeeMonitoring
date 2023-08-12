from typing import Annotated

from fastapi import APIRouter, Header

from ports.api.v1.schemas import ManagerListResponse


router = APIRouter(tags=["Managers"])


@router.get("/v1/managers")
async def get_managers(
    authorization: Annotated[str | None, Header()],
) -> ManagerListResponse:
    return ManagerListResponse(result=[])
