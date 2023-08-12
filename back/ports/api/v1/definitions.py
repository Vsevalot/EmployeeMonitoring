from fastapi import FastAPI
from services import TokenService
from storages import UserStorage, BusinessUnitStorage, CompanyStorage


class Application(FastAPI):
    token_service: TokenService | None = None
    user_storage: UserStorage | None = None
    business_unit_storage: BusinessUnitStorage | None = None
    company_storage: CompanyStorage | None = None
