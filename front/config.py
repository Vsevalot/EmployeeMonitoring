import os


class Config:
    BASE_URL = os.getenv("BASE_URL") or "localhost"
