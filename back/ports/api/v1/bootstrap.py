from ports.api.v1.definitions import Application
from .routers import ROUTERS


def get_application() -> Application:
    app = Application(title="Employee monitoring")
    for r in ROUTERS:
        app.include_router(r)
    return app
