import os


class Config:
    BASE_URL = os.getenv("BASE_URL") or "159.223.224.135:8000"
