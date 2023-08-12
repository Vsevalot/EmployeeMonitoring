from typing import Annotated

from fastapi import APIRouter, Header

from ports.api.v1.schemas import FactorsResponse


router = APIRouter(tags=["Factors"])


@router.get("/v1/factors")
async def get_factors(
    authorization: Annotated[str | None, Header()],
) -> FactorsResponse:
    return FactorsResponse(result=[])
