from .categories import router as factor_router
from .login import router as login_router
from .participant import router as participant_router
from .states import router as states_router
from .managers import router as manager_router
from .feedbacks import router as feedback_router
from .register import router as registration_router
from .instructions import router as instruction_router
from .recommendations import router as recommendation_router
from .fill import router as fill_router
from .cookie import router as cookie_router


ROUTERS = (
    factor_router,
    login_router,
    participant_router,
    states_router,
    manager_router,
    feedback_router,
    registration_router,
    instruction_router,
    recommendation_router,
    fill_router,
    cookie_router,
)
