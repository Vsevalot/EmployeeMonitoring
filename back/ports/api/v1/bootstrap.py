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

    origins = [
        # "http://localhost",
        # "http://localhost:8080",
        # "http://127.0.0.1",
        # "http://127.0.0.1:8080",
        # "http://159.223.224.135:8080",
        "http://159.223.224.135:8080/",
        # "http://159.223.224.135:8080/login",
        # "http://159.223.224.135:8080/login/",
        # "http://159.223.224.135:8080"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    for r in ROUTERS:
        app.include_router(r)
    return app
