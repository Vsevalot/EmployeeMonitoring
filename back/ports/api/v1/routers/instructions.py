from ports.api.v1.schemas import InstructionResponse
from fastapi import APIRouter, Depends

from domain.contracts import INSTRUCTION
from domain.entities import User
from ports.api.v1.dependencies import get_current_user


router = APIRouter(tags=["Instructions"])


@router.get("/v1/instructions")
async def get_instruction(
        user: User = Depends(get_current_user),
) -> InstructionResponse:
    return InstructionResponse(result=INSTRUCTION.format(name=user['first_name']))
