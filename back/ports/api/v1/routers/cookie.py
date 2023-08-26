from pydantic import BaseModel

from ports.api.v1.definitions import Request
import datetime

from fastapi import APIRouter, Response

router = APIRouter(tags=["Cookies"])


COOKIE_NAME = 'test-cookie'


@router.post("/api/v1/set-cookie")
async def generate_random_feedbacks(
        request: Request,
):
    res = Response(status_code=204)
    res.set_cookie(
        key=COOKIE_NAME,
        value='max-cookie',
        max_age=datetime.timedelta(days=100).seconds,
        httponly=True,
    )
    return res


class CookieResponse(BaseModel):
    cookie_is_set: bool


@router.get("/api/v1/is-cookie-set")
async def generate_random_feedbacks(
        request: Request,
) -> CookieResponse:
    if request.cookies.get(COOKIE_NAME) == 'max-cookie':
        return CookieResponse(cookie_is_set=True)
    return CookieResponse(cookie_is_set=False)
