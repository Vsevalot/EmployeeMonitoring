from fastapi import APIRouter, Depends

from ports.api.v1.schemas import ManagerListResponse, ManagerListItem
from domain.contracts import UserRole
from services import UserService
from ports.api.v1.dependencies import get_user_service

router = APIRouter(tags=["Managers"])


@router.get("/api/v1/managers")
async def get_managers(
    user_service: UserService = Depends(get_user_service),
) -> ManagerListResponse:
    managers = await user_service.get_list(filters={"role": UserRole.manager})
    return ManagerListResponse(result=[ManagerListItem(
        id=m['id'],
        first_name=m['first_name'],
        last_name=m['last_name'],
        surname=m['surname'],
        department=m['business_unit']['name'],
        company=m['business_unit']['company']['name'],
    ) for m in managers])
