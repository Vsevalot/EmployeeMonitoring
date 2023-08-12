from fastapi import APIRouter, Response, Depends

from ports.api.v1.schemas import ManagerRegisterBody, EmployeeRegisterBody
from storages import UserStorage, CompanyStorage, BusinessUnitStorage
from services import TokenService


router = APIRouter(tags=["Registration"])


@router.post("/v1/register/managers")
async def register_user(
    body: ManagerRegisterBody,
    # user_storage: UserStorage = Depends(get_user_storage),
    # company_storage: CompanyStorage = Depends(get_company_storage),
    # business_unit_storage: BusinessUnitStorage = Depends(get_business_unit_storage),
    # token_service: TokenService = Depends(get_token_service),
) -> Response:
    company_id = await company_storage.save(name=body.company)
    business_unit_id = await business_unit_storage.save(
        name=body.department,
        company_id=company_id,
    )
    user_id = await user_storage.save(
        **body.model_dump(exclude={"company", "department"}),
        business_unit_id=business_unit_id,
    )
    user = await user_storage.get(user_id)
    token = await token_service.get_token_for_user(user)
    return Response(content=token, status_code=201)


@router.post("/v1/register/employees")
async def register_user(
    body: EmployeeRegisterBody,
) -> Response:
    return Response(status_code=201)
