from .factors import router as factor_router
from .login import router as login_router
from .participant import router as participant_router
from .states import router as states_router
from .managers import router as manager_router
from .feedbacks import router as feedback_router
from .registration import router as registration_router
from .instructions import router as instruction_router


ROUTERS = (
    factor_router,
    login_router,
    participant_router,
    states_router,
    manager_router,
    feedback_router,
    registration_router,
    instruction_router,
)
