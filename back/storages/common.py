from sqlalchemy.ext.asyncio import AsyncConnection


class StorageRDBS:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection
