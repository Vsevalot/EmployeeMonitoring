from ports.api.v1.schemas import FactorsResponse, Category
from fastapi import APIRouter, Depends

from domain.entities import User
from services.category import CategoryService
from ports.api.v1.dependencies import get_current_user, get_category_service

router = APIRouter(tags=["Categories"])


@router.get("/v1/categories")
async def get_factors(
    category_service: CategoryService = Depends(get_category_service)
) -> FactorsResponse:
    categories = await category_service.get_categories()
    return FactorsResponse(result=[Category(**c) for c in categories])
