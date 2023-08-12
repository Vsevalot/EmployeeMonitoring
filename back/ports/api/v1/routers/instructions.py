from typing import Annotated

from fastapi import APIRouter, Header

from ports.api.v1.schemas import InstructionResponse


router = APIRouter(tags=["Factors"])


@router.get("/v1/instructions")
async def get_instruction(
    authorization: Annotated[str | None, Header()],
) -> InstructionResponse:
    return InstructionResponse(result="test")
