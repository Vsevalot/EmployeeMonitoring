from fastapi import APIRouter, Depends, Path, Response

from ports.api.v1.schemas import ManagerResponse, ManagerItem
from domain.contracts import UserRole
from services import UserService
from ports.api.v1.dependencies import get_user_service
import config


router = APIRouter(tags=["Managers"])


@router.get("/api/v1/managers/{code}")
async def get_manager(
    code: str = Path(
        max_length=config.MANAGER_CODE_LENGTH, min_length=config.MANAGER_CODE_LENGTH
    ),
    user_service: UserService = Depends(get_user_service),
) -> ManagerResponse:
    managers = await user_service.get_list(
        filters={"role": UserRole.manager, "code": code}
    )
    if not managers:
        return Response(status_code=404)
    if len(managers) > 1:
        raise ValueError(f"Invalid number of managers with given code: {code}")
    m = managers[0]
    return ManagerResponse(
        result=ManagerItem(
            id=m["id"],
            first_name=m["first_name"],
            last_name=m["last_name"],
            surname=m["surname"],
            department=m["business_unit"]["name"],
            company=m["business_unit"]["company"]["name"],
        )
    )
