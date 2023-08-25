from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI, Request as BaseRequest


class Application(FastAPI):
    engine: AsyncEngine


class Request(BaseRequest):
    app: Application
