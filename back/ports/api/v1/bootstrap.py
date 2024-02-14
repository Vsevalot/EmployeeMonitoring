from sqlalchemy.ext.asyncio import create_async_engine
from fastapi.middleware.cors import CORSMiddleware

from config import DBConfig
from ports.api.v1.definitions import Application
from repositories.common import AlreadyInUse, NotFoundError
from ext.http_tools import handler409, handler404
from .routers import ROUTERS


def get_application(db_config: DBConfig) -> Application:
    app = Application(title="Employee monitoring")
    app.engine = create_async_engine(db_config.dsn, echo=db_config.echo)

    app.add_exception_handler(AlreadyInUse, handler409)
    app.add_exception_handler(NotFoundError, handler404)

    for r in ROUTERS:
        app.include_router(r)
    return app
