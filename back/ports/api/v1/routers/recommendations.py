from ports.api.v1.schemas import RecommendationsResponse
from fastapi import APIRouter, Depends

from domain.contracts import RECOMMENDATIONS
from domain.entities import User
from ports.api.v1.dependencies import get_current_user


router = APIRouter(tags=["Recommendations"])


@router.get("/api/v1/recommendations")
async def get_instruction(
        user: User = Depends(get_current_user),
) -> RecommendationsResponse:
    return RecommendationsResponse(result=RECOMMENDATIONS.format(name=user['first_name']))
